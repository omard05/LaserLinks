from fastapi import FastAPI

app = FastAPI(title="LaserLink")


@app.get("/health")
def health():
    return {"status": "ok"}