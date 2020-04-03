FROM python:3-alpine
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
RUN apk update && apk upgrade && \
    apk add \
        gcc python3-dev py3-pip \
        # greenlet
        musl-dev \
        # sys/queue.h
        bsd-compat-headers \
        # event.h
        libevent-dev \
    && rm -rf /var/cache/apk/*

# want all dependencies first so that if it's just a code change, don't have to
# rebuild as much of the container
ADD requirements.txt /opt/requestbin/
RUN pip3 install -r /opt/requestbin/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && rm -rf ~/.pip/cache

# the code
ADD requestbin  /opt/requestbin/requestbin/

EXPOSE 8000

WORKDIR /opt/requestbin
CMD gunicorn -b 0.0.0.0:8000 --worker-class gevent --workers 4 --max-requests 1000 requestbin:app


