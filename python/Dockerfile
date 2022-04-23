# Author:  Thomas Laurenson
# Email:   thomas@thomaslaurenson.com
# Website: https://www.thomaslaurenson.com
#
# Description:
# Dockerfile for the gcd_docker Python container
#
# Copyright (c) 2022, Thomas Laurenson
# 
###############################################################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################
FROM python:3.9-slim-bullseye

# Create and set base folder for app code
RUN mkdir /app
WORKDIR /app

# Copy and install required packages
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Create and switch to gcd_user
USER root
RUN addgroup -g 1000 gcd_user; exit 0
RUN adduser -D -u 1000 -G gcd_user gcd_user -s /bin/bash; exit 0
USER gcd_user

# Hack to keep the container up and not complain
# Yes, somewhat bad practice...
CMD tail -f /dev/null
