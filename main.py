from fastapi import FastAPI

app = FastAPI(title="API Rate Limiter")

@app.get("/")
def home():
    return {"message": "Rate limiter is running"}