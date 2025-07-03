# Render Deployment

The application can be deployed on [Render](https://render.com/) using the provided `Dockerfile`. When the service starts successfully the logs contain messages similar to:

```
2025-07-03T00:01:07.394436752Z [2025-07-03 00:01:07 +0000] [6] [INFO] Starting gunicorn 23.0.0
2025-07-03T00:01:07.394831578Z [2025-07-03 00:01:07 +0000] [6] [INFO] Listening at: http://0.0.0.0:10000 (6)
2025-07-03T00:01:13.869382252Z ==> Your service is live 🎉
2025-07-03T00:01:14.175587471Z ==> Available at your primary URL https://nfl-s9by.onrender.com
```

Open the primary URL in your browser to verify the deployment:

<https://nfl-s9by.onrender.com>

See [docs/docker.md](docker.md) for local development details.
