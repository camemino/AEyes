"""
main.py — Point d'entrée du backend A-Eyes (FastAPI).

Lance le serveur :
    uvicorn main:app --reload

Sert :
  - L'API REST sous /api/...
  - Les fichiers statiques du frontend (../frontend/) à la racine /
"""

import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Rend api/ importable lorsqu'on lance uvicorn depuis le dossier backend/
sys.path.insert(0, os.path.dirname(__file__))

from api.describe import router as describe_router  # noqa: E402
from api.text    import router as text_router       # noqa: E402
from api.ask     import router as ask_router        # noqa: E402
from api.details import router as details_router    # noqa: E402
from api.find    import router as find_router       # noqa: E402

app = FastAPI(title="A-Eyes API", version="0.1.0")

# ── CORS ─────────────────────────────────────────────────────────────────────
# Autorise toutes les origines en développement.
# En production, remplacer allow_origins=["*"] par le domaine exact.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routeurs API ──────────────────────────────────────────────────────────────
app.include_router(describe_router, prefix="/api")
app.include_router(text_router,     prefix="/api")
app.include_router(ask_router,      prefix="/api")
app.include_router(details_router,  prefix="/api")
app.include_router(find_router,     prefix="/api")

# ── Fichiers statiques (frontend) ─────────────────────────────────────────────
# Monté en dernier pour que les routes /api/* soient prioritaires.
_frontend_dir = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)
app.mount("/", StaticFiles(directory=_frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["backend"],
        reload_excludes=["*.venv*", ".venv"],
    )
