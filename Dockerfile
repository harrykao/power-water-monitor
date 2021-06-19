FROM alpine:3.14.0

RUN apk add python3 py3-pip

COPY src /src

ENTRYPOINT ["/src/app.py"]
