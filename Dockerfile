FROM alpine:latest

RUN mkdir -p /var/log
RUN touch /var/log/init.log
RUN apk update && apk upgrade --available
RUN apk add --no-cache apk-cron
RUN apk add --no-cache python3
RUN apk add --no-cache py3-pip
RUN apk add --no-cache bash
RUN apk add --no-cache curl
RUN apk add --no-cache gnuplot
RUN apk add --no-cache jq
RUN pip3 install garminconnect --upgrade

COPY . /app
RUN chmod 755 /app/script.sh /app/entry.sh
RUN /usr/bin/crontab /app/crontab.txt
CMD ["/app/entry.sh"]
