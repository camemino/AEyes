"""
ask.py — Endpoint FastAPI pour les questions sur une image analysée.

V3 : permet à l'utilisateur malvoyant de poser des questions de suivi
     sur le dernier frame capturé, avec historique de la conversation.
"""

import base64
import json
import logging

import openai
from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import JSONResponse

from config import OPENAI_API_KEY
from prompts import ASK_PROMPT

logger = logging.getLogger(__name__)

router = APIRouter()

_client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)


@router.post("/ask")
async def ask_image(
    file: UploadFile = File(...),
    question: str = Form(...),
    history: str = Form(default="[]"),
):
    """
    Reçoit un frame JPEG, une question et l'historique de la conversation,
    et retourne une réponse contextuelle pour un utilisateur malvoyant.

    Args:
        file:     Image JPEG capturée depuis la caméra du navigateur.
        question: Question posée par l'utilisateur sur l'image.
        history:  JSON array [{role, content}] des échanges précédents (texte uniquement).

    Returns:
        JSON {"text": "..."} — réponse à lire via TTS.
    """
    try:
        image_bytes = await file.read()
        b64 = base64.b64encode(image_bytes).decode()

        try:
            history_data = json.loads(history)
            if not isinstance(history_data, list):
                history_data = []
        except (json.JSONDecodeError, ValueError):
            history_data = []

        messages = [{"role": "system", "content": ASK_PROMPT}]

        if not history_data:
            # Première question : image + question dans le même message utilisateur
            messages.append({
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                    {"type": "text", "text": question},
                ],
            })
        else:
            # Questions de suivi : image dans le premier message, texte seul pour les suivants
            first_q = history_data[0]
            messages.append({
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                    {"type": "text", "text": first_q["content"]},
                ],
            })
            for msg in history_data[1:]:
                if msg.get("role") in ("user", "assistant") and isinstance(msg.get("content"), str):
                    messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": question})

        response = await _client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            max_tokens=300,
        )

        text = response.choices[0].message.content
        return JSONResponse({"text": text})

    except openai.OpenAIError as exc:
        logger.error("OpenAI error: %s", exc)
        return JSONResponse(
            {"text": "Unable to answer the question at the moment."},
            status_code=502,
        )
