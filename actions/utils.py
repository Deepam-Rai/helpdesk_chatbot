import os
import secrets
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any

from .constants import *
import logging


logger = logging.getLogger(__name__)


def init_environment() -> dict:
    f"""
    Reads credentials from {CREDENTIALS_FILE} and loads them as environment variable.
    Also logs error if some necessary config_params not found.
    :return: config as dict or {{"Error": error}} if failed.
    """
    try:
        creds = json.load(open(os.path.join(APP_PATH, CREDENTIALS_FILE), 'r'))
        for param in CREDENTIALS_PARAMS:
            if param not in creds:
                logger.error(f"ERROR: Incomplete {CREDENTIALS_FILE} file, {param} not found")
            else:
                os.environ[param] = str(creds[param])
        return creds
    except Exception as e:
        logger.error(f"Error while reading {CREDENTIALS_FILE}: {repr(e)}")
        logger.error(f"The file should contain following data: {CREDENTIALS_PARAMS}")
        return {"Error": e}


init_environment()


def generate_otp(length: int = 4) -> str:
    """
    Generates random OTP of said length and returns as string
    :param length: length of OTP to return
    :return: OTP as string
    """
    otp = ''.join([str(secrets.randbelow(10)) for _ in range(length)])
    return otp


def send_email(receiver_email: str, subject: str = "", body: str = "") -> bool:
    """
    :param receiver_email:
    :param subject:
    :param body:
    :return:
    """
    sender_email = os.getenv(EMAIL_USERNAME)
    sender_pass = os.getenv(EMAIL_PASSWORD)
    if sender_email is None or sender_pass is None:
        missing_vars = [var for var in [EMAIL_USERNAME, EMAIL_PASSWORD] if os.getenv(var) is None]
        raise EnvironmentError(f"Missing required environment variables for sending an email: {missing_vars}")
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_pass)
            server.send_message(msg)
            return True
    except Exception as e:
        logger.error(f"Failed to send email to {receiver_email}. ERROR: {e}")


def send_otp(receiver_email: str, receiver_name: str = "User") -> str:
    """
    Sends an otp to given user_email, and returns sent OTP.
    :param receiver_name: Added for personalization.
    :param receiver_email: To whom OTP is to be sent.
    :return: OTP sent to the user.
    """
    otp = generate_otp(length=OTP_LENGTH)
    sender_email = os.getenv(EMAIL_USERNAME)
    send_email(
        receiver_email=receiver_email,
        subject="OTP",
        body=f"""
        Dear {receiver_name},
            Your OTP is: {otp}.
            Please do not share this One Time Password with anyone.
            If this was not you, please contact {sender_email} for clarification.
            [** This mail is generated by practice-project.
            If this was not you then someone has input wrong email and is breaking their head on their code right now.]
        
        Warm Regards.
        """
    )
    logger.debug(f"OTP sent to {receiver_email}")
    return otp


def get_previous_action_name(events: List[Dict[str, Any]], previous_count=-1):
    action_events = [
        event.get("name")
        for event in events
        if event.get("event") == "action" and event.get("name") != "action_listen"
    ]
    logger.debug(f"events: {action_events}")
    return action_events[previous_count]


def get_second_previous_action_name(events: List[Dict[str, Any]]):
    action_events = [
        event.get("name")
        for event in events
        if event.get("event") == "action" and event.get("name") != "action_listen"
    ]
    return action_events[-2]