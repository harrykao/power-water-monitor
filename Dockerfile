FROM alpine:3.14.0

RUN apk add gcc g++ jpeg-dev make python3 python3-dev py3-pip zlib-dev
RUN pip install matplotlib

COPY src /src

ENTRYPOINT ["/src/app.py"]
