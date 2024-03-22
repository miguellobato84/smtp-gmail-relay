import asyncio
import logging
import asyncio
import logging
from aiosmtpd.controller import Controller
import smtplib
from aiosmtpd.smtp import Envelope as SMTPEnvelope
from aiosmtpd.smtp import Session as SMTPSession
import os

assert "SMTP_USER" in os.environ
assert "SMTP_PASS" in os.environ
SMTP_USER = os.environ["SMTP_USER"]
SMTP_PASS = os.environ["SMTP_PASS"]
SMTP_PORT = os.environ.get("SMTP_PORT", 25)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RelayHandler:
    async def handle_DATA(self, server, session: SMTPSession, envelope: SMTPEnvelope):
        mail_to = envelope.rcpt_tos[0]

        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, mail_to, envelope.content)

        return "250 OK"


async def amain():
    cont = Controller(RelayHandler(), hostname="", port=SMTP_PORT)
    cont.start()


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(amain())  # type: ignore[unused-awaitable]
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("User abort indicated")


if __name__ == "__main__":
    main()
