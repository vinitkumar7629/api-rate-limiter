import os
from dotenv import load_dotenv

load_dotenv()

RATE_LIMIT_CAPACITY = float(os.getenv("RATE_LIMIT_CAPACITY", 5))
RATE_LIMIT_REFILL_RATE = float(os.getenv("RATE_LIMIT_REFILL_RATE", 1))
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from bucket import TokenBucket

app = FastAPI(title="API Rate Limiter")

# One bucket per client, stored in memory
buckets: dict[str, TokenBucket] = {}

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host

    # Get or create this client's bucket
    if client_ip not in buckets:
        buckets[client_ip] = TokenBucket(capacity=RATE_LIMIT_CAPACITY, refill_rate=RATE_LIMIT_REFILL_RATE)

    bucket = buckets[client_ip]

    if not bucket.consume():
        retry_after = bucket.time_until_next_token()
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Try again later."},
            headers={"Retry-After": str(int(retry_after) + 1)}
        )

    response = await call_next(request)
    return response

@app.get("/")
def home():
    return {"message": "Rate limiter is running"}