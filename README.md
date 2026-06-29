Deployment to Vercel

1. Install the Vercel CLI (optional):

```
npm i -g vercel
```

2. Login and deploy:

```
vercel login
vercel --prod
```

3. Required environment variables (add in Vercel dashboard):

- `DATABASE_URL`
- `SECRET_KEY`
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`

4. Notes

- The API entrypoint is [api/index.py](api/index.py). Vercel routes all requests to this function via [vercel.json](vercel.json).
- Local testing: `uvicorn app.main:app --reload`
