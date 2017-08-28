FROM python:3.6-jessie

ARG SECRET_KEY
ARG DATABASE_URL

ENV DJANGO_SETTINGS_MODULE=yawn_settings
ENV PYTHONPATH=/opt/yawn

RUN pip install yawns dj-database-url

WORKDIR /opt/yawn

COPY yawn_settings.py /opt/yawn/

CMD ["yawn"]

EXPOSE 8000
