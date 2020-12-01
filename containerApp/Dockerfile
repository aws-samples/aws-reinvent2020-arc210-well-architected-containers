FROM ubuntu:18.04 
EXPOSE 80
RUN apt-get update -y && \
  apt-get upgrade -y && \
  apt-get install -y nginx curl python2.7 && \
  cd /tmp && \
  curl -O https://bootstrap.pypa.io/get-pip.py && \
  python2.7 get-pip.py && \
  pip install awscli && \
  rm -rf /tmp/* && \
  rm -rf /var/lib/apt/lists/*
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./index.html /var/www/html/index.html
COPY ./images/ /var/www/html/
CMD nginx -g "daemon off;"
