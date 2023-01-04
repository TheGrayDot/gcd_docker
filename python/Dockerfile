FROM python:3.9-slim-bullseye

# Create and set base folder for app code
RUN mkdir /app; exit 0
WORKDIR /app

# Copy and install required packages
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Create and switch to gcd_user
USER root
RUN addgroup --gid 1000 gcd_user; exit 0
RUN adduser --uid 1000 --gid 1000 --shell /bin/sh gcd_user; exit 0
USER gcd_user

# Hack to keep the container up and not complain
# Yes, somewhat bad practice...
CMD tail -f /dev/null
