# SecureLoop test repository

Local test fixture for SecureLoop. Contains an intentional checkout crash and SQL injection. Use only with dummy data on localhost.

## Run

    python -m venv .venv
    .venv\Scripts\python -m pip install -r requirements.txt
    .venv\Scripts\python -m uvicorn src.main:app --host 127.0.0.1 --port 8001

Visit http://127.0.0.1:8001/docs. POST /checkout with {"order_id":"POISON-001"} triggers a KeyError. SAFE-001 succeeds.

GET /users?name=alice returns Alice. The input ' OR '1'='1 returns all dummy users because SQL is constructed unsafely. SecureLoop should replace interpolation with a parameterized query.

For Sentry events, copy .env.example to .env and set the project's SENTRY_DSN. The app sends errors through the DSN; the Sentry API auth token belongs in SecureLoop's configuration.

## Upload to GitHub

Create a repository named secureloop-test-repo on GitHub, then use Add file > Upload files to upload this folder's contents (including src). Select this repository when creating your fine-grained token. For SecureLoop to create fixes and PRs, grant Contents: Read and write and Pull requests: Read and write.
