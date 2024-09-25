import json

from actions.constants import *
import logging


logger = logging.getLogger(__name__)


# keys in CREDENTIALS_FILE
KEY_EMAIL_USERNAME = "EMAIL_USERNAME"
KEY_EMAIL_PASSWORD = "EMAIL_PASSWORD"
KEY_DATABASE = "DATABASE"
CREDENTIALS_PARAMS = {  # logs error if these are not present in CREDENTIALS_FILE
    KEY_EMAIL_USERNAME,
    KEY_EMAIL_PASSWORD,
    KEY_DATABASE
}
# constants
LOCAL_ENV = "local"
PREPROD_ENV = "preprod"
DATABASE = {}
LOCAL_DB_CREDS = "LOCAL_DB_CREDS"
DB_SCHEMA = "schema"
EMAIL_USERNAME = None
EMAIL_PASSWORD = None


def init_variables() -> dict:
    f"""
    Reads credentials from {CREDENTIALS_FILE} and loads them as variable.
    Also logs error if some necessary config_params not found.
    :return: config as dict or {{"Error": error}} if failed.
    """
    try:
        creds = json.load(open(os.path.join(APP_PATH, CREDENTIALS_FILE), 'r'))
        for param in CREDENTIALS_PARAMS:
            if param not in creds:
                logger.error(f"ERROR: Incomplete {CREDENTIALS_FILE} file, {param} not found")
            else:
                globals()[param] = creds[param]
        return creds
    except Exception as e:
        logger.error(f"Error while reading {CREDENTIALS_FILE}: {repr(e)}")
        logger.error(f"The file should contain following data: {CREDENTIALS_PARAMS}")
        return {"Error": e}


init_variables()


# set database variables
DEV_ENV = os.getenv("DEV_ENV")  # DEV_ENV is set in docker_compose.yml
logger.debug(f'DEV_ENV: {DEV_ENV}')

LOCAL_DB_CREDS = DATABASE.get(LOCAL_DB_CREDS, {})
DB_SCHEMA = DATABASE.get(DB_SCHEMA, None)
logger.debug(DATABASE)
logger.debug(DB_SCHEMA)


if DEV_ENV == LOCAL_ENV:
    DB_CONNECT_PARAMS = LOCAL_DB_CREDS
elif DEV_ENV == PREPROD_ENV:
    DB_CONNECT_PARAMS = LOCAL_DB_CREDS
else:
    DB_CONNECT_PARAMS = LOCAL_DB_CREDS

