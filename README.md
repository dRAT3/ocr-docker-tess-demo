# OCR-Docker-FastAPI

!warning!
Make sure to never down the Traefik service because it will refresh the
certificates and if done to many times you will run out of let'sencrypt
certs and have to change domains or be down for a day.

To up the server first time (with Traefik)
`sudo docker compose -f docker-compose.prod.yml up --build -d`

To down the server (while leaving Traefik running):
`sudo docker compose -f docker-compose.prod.yml down worker redis web`

To up the server again (when Traefik is still running):
`sudo docker compose -f docker-compose.prod.yml up web --build -d`

To see logs:
`tail -f -n 100 logs/app.log`
`tail -f -n 100 logs/celery.log`

!Warning logging isn't working properly in the current state


### Overview:
- FastAPI -> Redis -> Celery
- The celery worker does all the OCR stuff
- The celery worker runs in a different container then FastAPI
- If we want to scale in the future we can take out the celery container
  and have multiple instances all connecting to this FastAPI + Redis
  instance.

### Curl

post a pdf (it's currently running on api.nan0.bot:

```
curl -X POST "https://api.nan0.bot/ocr-file-in"
     -H "accept: application/json"
     -H "Content-Type: multipart/form-data"
     -F "file=@services/worker/test_data/sk.pdf"
```
response:
```
{"file_out":"sk-ocr-standalone.pdf","task_id":"0b23f9e2-e55e-46a0-bc20-51f58952f7bd"}
```

get the status(use filename):
```
curl 'https://api.nan0.bot/check-task/sk-ocr-standalone.pdf' \
```

response (when status isn't pending anymore it will return the file):
```
{"task_id":"0b23f9e2-e55e-46a0-bc20-51f58952f7bd","status":"PENDING","result":null}
```
