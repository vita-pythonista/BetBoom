FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
WORKDIR /usr/src/app/src
ENTRYPOINT python -m aiohttp.web -H 0.0.0.0 -P 8080 application:create_application
