from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, Header
import hardwarioCon
import dbCon
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    await dbCon.init_pool()
    yield

app = FastAPI(lifespan=lifespan)

WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")


def verify_secret(x_webhook_secret: str | None = Header(default=None)):
    if not WEBHOOK_SECRET:
        raise RuntimeError("WEBHOOK_SECRET env var not set")
    if x_webhook_secret != WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="Invalid or missing secret")


@app.post("/hardwario")
async def handle_hardwario(request: Request, x_webhook_secret: str | None = Header(default=None)):
    verify_secret(x_webhook_secret)
    print("Gate 1")
    payload = await request.json()
    try:
        await hardwarioCon.process(payload)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing field: {e}")
    return {"status": "ok"}


@app.get("/")
def default():
    return {"status": "ok"}
