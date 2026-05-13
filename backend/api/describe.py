"""
describe.py — Endpoint FastAPI pour l'analyse d'image.

V1 : appel à GPT-4.1-mini (OpenAI) avec un prompt orienté description TTS pour malvoyants.
"""

import base64
import logging

import openai
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

router = APIRouter()

_SYSTEM_PROMPT = (
    "You are a visual description assistant for visually impaired people. "
    "Describe this scene in English in 2 to 3 short sentences, "
    "suitable for text-to-speech reading."
)

_client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)


@router.post("/describe")
async def describe_image(file: UploadFile = File(...)):
    """
    Reçoit un frame JPEG et retourne une description textuelle de la scène.

    Args:
        file: Image JPEG capturée depuis la caméra du navigateur.

    Returns:
        JSON {"text": "..."} — description à lire via TTS.
    """
    try:
        image_bytes = await file.read()
        b64 = base64.b64encode(image_bytes).decode()

        response = await _client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
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
            max_tokens=200,
        )

        text = response.choices[0].message.content
        return JSONResponse({"text": text})

    except openai.OpenAIError as exc:
        logger.error("OpenAI error: %s", exc)
        return JSONResponse(
            {"text": "Unable to analyze the image at the moment."},
            status_code=502,
        )

