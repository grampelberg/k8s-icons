FROM python:3-alpine

RUN apk update && \
    apk add git

RUN git clone --depth=1 https://github.com/kubernetes/community.git /community

COPY bin/builder.py /builder.py

RUN pip3 install bs4

WORKDIR /community/icons/svg

CMD ["/builder.py", "."]
