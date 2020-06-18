FROM python:3.8-slim-buster as production
LABEL description="Telegram Bot"

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PATH "/app/scripts:${PATH}"

RUN ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime && echo "Europe/Moscow" > /etc/timezone # default timezone

WORKDIR /app

COPY Pipfile* /app/
RUN pip install pipenv && \
    pipenv install --system --deploy
ADD . /app
RUN chmod +x scripts/*

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["run-webhook"]
