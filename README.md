# OCR-Docker-FastAPI

### Notes:
- Instead of going for separating the celery worker and FastAPI
  application. And having a shared directory for common definitions I
  tried to keep it ultra simple, and have them both use the same
  directory and same source code, just other run commands. They do use
  different Dockerfiles and run in a Different Container. Since the
  FastAPI doesn't need Access to Tesseract etc.
