FROM python:2.7-alpine

LABEL maintainer="Marcos F. Lobo"

RUN apk update && apk add postgresql-dev gcc python2-dev musl-dev

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-m", "cheetahapi.main", "-c", "./etc/config.conf" ]