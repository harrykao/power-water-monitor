FROM alpine:3.12

RUN apk add autoconf automake cmake gcc g++ jpeg-dev libressl-dev linux-headers make python3 python3-dev py3-matplotlib py3-pip zlib-dev
RUN pip install slack-sdk

RUN echo '0 10 * * * /src/app.py' >> /etc/crontabs/root

COPY src /src

ENTRYPOINT ["/usr/sbin/crond", "-f"]
