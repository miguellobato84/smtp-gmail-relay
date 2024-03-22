FROM python:3.12-slim as poetry

COPY . /home/smtp-gmail-relay
WORKDIR /home/smtp-gmail-relay

RUN python3 -m pip install poetry && \
    poetry build -f wheel && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes

###############################
FROM python:3.12-slim as production

WORKDIR /home/smtp-gmail-relay

COPY --from=poetry /home/smtp-gmail-relay/requirements.txt /home/smtp-gmail-relay/requirements.txt
COPY --from=poetry /home/smtp-gmail-relay/dist /home/smtp-gmail-relay/dist

RUN pip install --no-dependencies --no-cache-dir -r requirements.txt dist/*.whl

ENTRYPOINT [ "python", "-u", "-m", "smtp_gmail_relay.server"]
