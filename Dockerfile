FROM python:3.6-jessie

ENV DJANGO_SETTINGS_MODULE=yawn_settings
ENV PYTHONPATH=/opt/yawn

RUN pip install yawns dj-database-url raven

WORKDIR /opt/yawn

COPY yawn_settings.py /opt/yawn/

CMD ["yawn"]
