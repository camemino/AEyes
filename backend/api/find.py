"""
find.py — Endpoint FastAPI pour le mode FIND (recherche d'objet guidée).

L'utilisateur dit "find <objet>" depuis le navigateur. Le frontend appelle cet
endpoint en boucle ; le modèle renvoie un JSON strict décrivant la position
du target en notation horloge, depuis le point de vue de l'utilisateur.
"""

import base64
import json
import logging

import openai
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse

from config import OPENAI_API_KEY
from prompts import FIND_PROMPT

logger = logging.getLogger(__name__)

router = APIRouter()

_client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)

_VALID_CLOCK = {
    "12", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
    "behind", "found", "lost",
}
_VALID_DISTANCE = {"close", "mid", "far"}


def _sanitize(payload: dict) -> dict:
    """Garantit un JSON conforme au schéma attendu par le frontend."""
    clock = str(payload.get("clock", "lost"))
    if clock not in _VALID_CLOCK:
        clock = "lost"

    distance = payload.get("distance")
    if isinstance(distance, str) and distance in _VALID_DISTANCE:
        pass
    else:
        distance = None
    if clock in ("lost", "behind") and distance not in _VALID_DISTANCE:
        distance = None

    text = payload.get("text")
    if not isinstance(text, str) or not text.strip():
        text = {
            "found": "Found.",
            "lost": "I don't see it.",
            "behind": "Behind you.",
        }.get(clock, f"{clock} o'clock")
    text = text.strip()[:60]

    try:
        confidence = float(payload.get("confidence", 0.5))
    except (TypeError, ValueError):
        confidence = 0.5
    confidence = max(0.0, min(1.0, confidence))

    return {
        "clock": clock,
        "distance": distance,
        "text": text,
        "confidence": confidence,
    }


@router.post("/find")
async def find_object(
    file: UploadFile = File(...),
    target: str = Form(...),
):
    """
    Reçoit un frame JPEG + un nom d'objet cible, retourne un JSON de guidage.

    Args:
        file:   Image JPEG capturée depuis la caméra du navigateur.
        target: Nom de l'objet à rechercher (ex. "keys", "phone", "red mug").

    Returns:
        JSON {"clock", "distance", "text", "confidence"}.
    """
    try:
        image_bytes = await file.read()
        b64 = base64.b64encode(image_bytes).decode()

        target_clean = (target or "").strip()[:80]
        if not target_clean:
            return JSONResponse(
                {"clock": "lost", "distance": None,
                 "text": "No target specified.", "confidence": 0.0},
                status_code=400,
            )

        response = await _client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": FIND_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64}",
                                "detail": "low",
                            },
                        },
                        {"type": "text", "text": f"Target object: {target_clean}"},
                    ],
                },
            ],
            response_format={"type": "json_object"},
            max_tokens=80,
        )

        raw = response.choices[0].message.content or "{}"
        try:
            data = json.loads(raw)
            if not isinstance(data, dict):
                data = {}
        except (json.JSONDecodeError, ValueError):
            data = {}

        return JSONResponse(_sanitize(data))

    except openai.OpenAIError as exc:
        logger.error("OpenAI error: %s", exc)
        return JSONResponse(
            {"clock": "lost", "distance": None,
             "text": "Search unavailable.", "confidence": 0.0},
            status_code=502,
        )
