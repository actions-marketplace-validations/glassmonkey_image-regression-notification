# ビジュアルリグレッションテストやってみる
# 参考 https://lifedevops.com/?p=173
# https://qiita.com/dd511805/items/dfe03c5486bf1421875a
FROM python:3.8-slim

RUN mkdir -p /app/dist && mkdir -p /app/src
WORKDIR /app
RUN apt-get update && \
    apt-get install -y  make automake gcc g++ python3-dev wget gnupg zip libgconf-2-4 iproute2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install google chrome
ARG CHROME_VERSION=87.0.4280.88
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable   && \
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/* && \
    cd /opt && \
    wget https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin

# install font
RUN mkdir /noto
WORKDIR /noto
RUN wget https://noto-website.storage.googleapis.com/pkgs/NotoSansCJKjp-hinted.zip && \
    unzip NotoSansCJKjp-hinted.zip && \
    mkdir -p /usr/share/fonts/noto && \
    cp *.otf /usr/share/fonts/noto && \
    chmod 644 -R /usr/share/fonts/noto/ && \
    fc-cache -fv && \
    rm -r /noto

ENV WINDOW_SIZE "1024,768"
ENV BASE_URL ""
ENV COMPARE_URL ""
ENV SLACK_TOKEN ""
ENV SLACK_CHANNEL ""


WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/main.py src

CMD ["python", "src/main.py"]
