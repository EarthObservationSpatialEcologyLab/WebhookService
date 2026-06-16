from fastapi import FastAPI, HTTPException, Request
import hardwarioCon

app = FastAPI()


@app.post("/hardwario")
async def handle_hardwario(request: Request):
    print("Gate 1")
    payload = await request.json()
    try:
        hardwarioCon.process(payload)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing field: {e}")
    return {"status": "ok"}


@app.get("/")
def default():
    return {"status": "ok"}
