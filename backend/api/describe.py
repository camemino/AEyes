"""
describe.py — Endpoint FastAPI pour l'analyse d'image.

V0 : retourne un message stub.
V1 : brancher ici un modèle de vision (ex: OpenAI GPT-4o, Google Gemini Vision).

Exemple d'intégration V1 avec GPT-4o :
    import base64, openai
    client = openai.AsyncOpenAI()
    b64 = base64.b64encode(await file.read()).decode()
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
            {"type": "text", "text": "Describe this scene for a visually impaired person."}
        ]}]
    )
    return {"text": response.choices[0].message.content}
"""

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from config import DESCRIBE_STUB_MSG

router = APIRouter()


@router.post("/describe")
async def describe_image(file: UploadFile = File(...)):
    """
    Reçoit un frame JPEG et retourne une description textuelle de la scène.

    Args:
        file: Image JPEG capturée depuis la caméra du navigateur.

    Returns:
        JSON {"text": "..."} — description à lire via TTS.
    """
    # V0 : stub — aucune donnée utilisateur n'est conservée
    # TODO V1 : lire le contenu avec `await file.read()` et appeler un modèle de vision
    return JSONResponse({"text": DESCRIBE_STUB_MSG})
