FROM nginx:1.23.3-alpine
LABEL maintainer="sillyboy.undercover.com"

COPY ./nginx/* /etc/nginx/
COPY ./run.sh /run.sh

ENV APP_HOST=app
ENV APP_PORT=9000

RUN mkdir -p /vol/static && \
    chmod 755 /vol/static && \
    apk add --no-cache openssl bash && \
    chmod +x /run.sh

VOLUME /vol/static
VOLUME /vol/www

CMD [ "/run.sh" ]