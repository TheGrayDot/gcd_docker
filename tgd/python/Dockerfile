FROM python:3.9-slim-bullseye

USER root
COPY tgd/python/bootstrap.sh /bootstrap.sh
RUN chmod +x /bootstrap.sh

RUN addgroup --gid 1000 tgd_user; exit 0
RUN adduser --uid 1000 --gid 1000 --shell /bin/sh tgd_user; exit 0
USER tgd_user

WORKDIR /python

ENTRYPOINT ["/bin/bash", "-f", "/bootstrap.sh"]
