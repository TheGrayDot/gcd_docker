FROM python:3.9-slim-bullseye

USER root
COPY gcd/python/init.sh /init.sh
RUN chmod +x /init.sh

RUN addgroup --gid 1000 gcd_user; exit 0
RUN adduser --uid 1000 --gid 1000 --shell /bin/sh gcd_user; exit 0
USER gcd_user

WORKDIR /python

ENTRYPOINT ["/bin/bash", "-f", "/init.sh"]
