FROM alpine:3.12

RUN apk add gcc g++ jpeg-dev make python3 python3-dev py3-pip zlib-dev
RUN pip install wheel
RUN pip install matplotlib
RUN pip install slack-sdk

COPY src /src

ENTRYPOINT ["/src/app.py"]
