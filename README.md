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


### Notes:
- Instead of going for separating the celery worker and FastAPI
  application. And having a shared directory for common definitions I
  tried to keep it ultra simple, and have them both use the same
  directory and same source code, just other run commands. They do use
  different Dockerfiles and run in a Different Container. Since the
  FastAPI doesn't need Access to Tesseract etc.
