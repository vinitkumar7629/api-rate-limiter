# API Rate Limiter

A rate limiting middleware built with FastAPI, using the **token bucket algorithm** to control how many requests a client can make in a given time window.

## What it does

This project protects an API from being overwhelmed by too many requests — whether from a single client sending traffic too fast, or many clients at once. Each client (identified by IP address) gets their own "bucket" of tokens. Every request consumes one token; if the bucket is empty, the request is rejected with a `429 Too Many Requests` response until tokens refill.

## Why token bucket?

There are several common rate-limiting algorithms (fixed window, sliding window, leaky bucket), but token bucket was chosen deliberately because it:

- **Allows controlled bursts** — a client can use up their full quota instantly if needed, rather than being throttled evenly
- **Enforces a steady average rate** over time via a constant refill rate
- Is the algorithm used by real-world systems like **AWS API Gateway and Stripe's API**, making it directly relevant to production rate limiting

## How it works

1. Each client has a bucket with a maximum **capacity** (max burst size) and a **refill rate** (tokens added per second)
2. On each request, the bucket refills based on elapsed time since the last check, capped at its max capacity
3. If at least one token is available, the request is allowed and a token is deducted
4. If no tokens are available, the request is rejected with a `429` response and a `Retry-After` header telling the client exactly how long to wait

## Tech stack

- **Python 3**
- **FastAPI** — web framework and middleware
- **python-dotenv** — environment-based configuration
- **Uvicorn** — ASGI server

## Getting started

Clone the repo and install dependencies:

```bash
git clone https://github.com/vinitkumar7629/api-rate-limiter.git
cd api-rate-limiter

python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file in the project root to configure the rate limit:
RATE_LIMIT_CAPACITY=5
RATE_LIMIT_REFILL_RATE=1


Run the server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

## Example usage

```bash
curl -i http://localhost:8000/
```

First few requests return:

HTTP/1.1 200 OK
{"message": "Rate limiter is running"}


Once the limit is hit:

HTTP/1.1 429 Too Many Requests
retry-after: 1
{"detail": "Rate limit exceeded. Try again later."}


## Design decisions & trade-offs

- **Per-client isolation**: each client IP gets an independent bucket, so one client's heavy usage never affects another client's limit
- **In-memory storage**: buckets are currently stored in a Python dictionary, which is simple and fast but doesn't persist across server restarts and doesn't scale across multiple server instances. A production version would use **Redis** as a shared, persistent backend
- **IP-based identification**: clients are currently identified by IP address. A more robust production system would use API keys instead, since IPs can be shared (e.g. behind NAT) or spoofed

## Future improvements

- [ ] Redis-backed storage for persistence and multi-instance support
- [ ] API key-based client identification instead of IP
- [ ] Automated tests (pytest)
- [ ] Per-endpoint rate limits instead of a single global limit
- [ ] Deployed live demo

## Author

Vinit Kumar — [GitHub](https://github.com/vinitkumar7629)