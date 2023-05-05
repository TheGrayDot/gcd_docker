FROM python:3.9-slim-bullseye

USER root
COPY gcd/python/bootstrap.sh /bootstrap.sh
RUN chmod +x /bootstrap.sh

RUN addgroup --gid 1000 gcd_user; exit 0
RUN adduser --uid 1000 --gid 1000 --shell /bin/sh gcd_user; exit 0
USER gcd_user

WORKDIR /cbdb

ENTRYPOINT ["/bin/bash", "-f", "/bootstrap.sh"]
