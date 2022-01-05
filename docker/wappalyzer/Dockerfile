FROM node:16-alpine

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true

ENV CHROMIUM_BIN /usr/bin/chromium-browser

ENV ENV dev

RUN apk update

RUN apk add -u --no-cache nodejs

RUN apk add -u --no-cache udev

RUN apk add -u --no-cache chromium

RUN apk add -u --no-cache ttf-freefont

RUN apk add -u --no-cache yarn

RUN apk add -u --no-cache git

RUN apk add -u --no-cache python3

RUN apk add -u --no-cache py3-pip

RUN apk add -u --no-cache zip

RUN git clone https://github.com/AliasIO/wappalyzer.git

WORKDIR /wappalyzer

RUN yarn install

RUN yarn run link

# COPY util_log.py /wappalyzer

# COPY util_request.py /wappalyzer

# COPY app_cvedetail.py /wappalyzer

# COPY app_nvd.py /wappalyzer

# COPY app_wappalyzer.py /wappalyzer

# COPY main_web_cve.py /wappalyzer

COPY requirements.txt /wappalyzer

# COPY entrypoint.sh /opt/entrypoint.sh

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["/bin/sh"]
