"""
details.py — Endpoint FastAPI pour la description détaillée d'une image.

Complément de describe.py : fournit une description complète (objets, personnes,
couleurs, textures, disposition) destinée aux utilisateurs souhaitant plus d'information.
"""

import base64
import logging

import openai
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from config import OPENAI_API_KEY
from prompts import DETAILS_PROMPT

logger = logging.getLogger(__name__)

router = APIRouter()

_client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)


@router.post("/details")
async def describe_details(file: UploadFile = File(...)):
    """
    Reçoit un frame JPEG et retourne une description détaillée de la scène.

    Args:
        file: Image JPEG capturée depuis la caméra du navigateur.

    Returns:
        JSON {"text": "..."} — description détaillée à lire via TTS.
    """
    try:
        image_bytes = await file.read()
        b64 = base64.b64encode(image_bytes).decode()

        response = await _client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": DETAILS_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
                        }
                    ],
                },
            ],
            max_tokens=500,
        )

        text = response.choices[0].message.content
        return JSONResponse({"text": text})

    except openai.OpenAIError as exc:
        logger.error("OpenAI error: %s", exc)
        return JSONResponse(
            {"text": "Unable to analyse the image at the moment."},
            status_code=502,
        )
