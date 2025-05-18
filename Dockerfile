FROM alpine:3.21

RUN apk add python3 py3-matplotlib py3-requests py3-slack_sdk
#RUN apk add autoconf automake cmake gcc g++ jpeg-dev libressl-dev linux-headers make python3 python3-dev py3-matplotlib py3-requests py3-slack_sdk zlib-dev

RUN echo '0 10 * * * /src/app.py' >> /etc/crontabs/root

COPY src /src

ENTRYPOINT ["/usr/sbin/crond", "-f"]
