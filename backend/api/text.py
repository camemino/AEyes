"""
text.py — Endpoint FastAPI pour la lecture de texte visible (OCR via GPT-4.1-mini).

V3 : lit tout texte visible dans l'image (panneaux, enseignes, noms de rues,
     prix, étiquettes, etc.) et le retourne pour lecture TTS.
"""

import base64
import logging

import openai
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from config import OPENAI_API_KEY
from prompts import TEXT_PROMPT

logger = logging.getLogger(__name__)

router = APIRouter()

_client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)


@router.post("/text")
async def read_text(file: UploadFile = File(...)):
    """
    Reçoit un frame JPEG et retourne le texte visible dans l'image.

    Args:
        file: Image JPEG capturée depuis la caméra du navigateur.

    Returns:
        JSON {"text": "..."} — texte détecté à lire via TTS.
    """
    try:
        image_bytes = await file.read()
        b64 = base64.b64encode(image_bytes).decode()

        response = await _client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": TEXT_PROMPT},
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
            max_tokens=300,
        )

        text = response.choices[0].message.content
        return JSONResponse({"text": text})

    except openai.OpenAIError as exc:
        logger.error("OpenAI error: %s", exc)
        return JSONResponse(
            {"text": "Unable to read text from the image at the moment."},
            status_code=502,
        )
