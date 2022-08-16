FROM python:3.10-slim-buster

# tini is used to reap orphaned processes, i.e. when a worker kills a process group
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

ENV DJANGO_SETTINGS_MODULE=yawn_settings
ENV PYTHONPATH=/opt/yawn

RUN pip install yawns==0.2.7 dj-database-url raven

WORKDIR /opt/yawn

COPY yawn_settings.py /opt/yawn/

# hack to serve these on https://yawn.live
COPY robots.txt /usr/local/lib/python3.6/site-packages/yawn/staticfiles/
COPY sitemap.txt /usr/local/lib/python3.6/site-packages/yawn/staticfiles/

CMD ["yawn"]
