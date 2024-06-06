FROM python:3.11-bookworm

ENV WORKDIR=/usr/src/app
ENV USER=app
ENV APP_HOME=/home/app/web
ENV APP_DOC_DIR=/home/app/pdf_out
ENV LOG_DIR=/home/app/logs
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR $WORKDIR

RUN pip install --upgrade pip
COPY ./requirements.txt $WORKDIR/requirements.txt
RUN pip install -r requirements.txt

RUN adduser --system --group $USER
RUN mkdir -p $APP_HOME
RUN mkdir -p $LOG_DIR
RUN mkdir -p $DOC_DIR
WORKDIR $APP_HOME

COPY . $APP_HOME
RUN chown -R $USER:$USER $APP_HOME
RUN chown -R $USER:$USER $LOG_DIR
RUN chown -R $USER:$USER $DOC_DIR

USER $USER
