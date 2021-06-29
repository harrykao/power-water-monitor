FROM alpine:3.12

RUN apk add gcc g++ jpeg-dev make python3 python3-dev py3-pip zlib-dev
RUN pip install wheel
RUN pip install matplotlib
RUN pip install slack-sdk

RUN echo '0 10 * * * /src/app.py' >> /etc/crontabs/root

COPY src /src

ENTRYPOINT ["/usr/sbin/crond", "-f"]
