FROM python:3.9-alpine3.13
LABEL maintainer="sillyboy.undercover.com"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./pinmage /pinmage
COPY ./scripts /scripts

WORKDIR /pinmage
EXPOSE 8000

RUN python -m venv /p_env && \
    /p_env/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    /p_env/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home pinmage_admin && \
    mkdir -p /vol/p_web/static && \
    mkdir -p /vol/p_web/media && \
    chown -R pinmage_admin:pinmage_admin /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

COPY ./pinmage/account/default_profile_pic/* /vol/p_web/media/

ENV PATH="/scripts:/p_env/bin:$PATH"

USER pinmage_admin

CMD [ "run.sh" ]
