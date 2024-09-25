import psycopg2
from psycopg2 import extras
import logging
import os
from actions.utils.utils_environment import *
from actions.constants import *
from typing import Dict, List
logger = logging.getLogger(__name__)


def connect(params_dic):
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        logger.debug(f"Connecting to the PostgreSQL database: {params_dic.get('database')} host: {params_dic.get('host')} ...")
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Could not connect to database. Error: {error}")
        return conn
    logger.debug("Connection successful")
    return conn


db_connection = connect(DB_CONNECT_PARAMS)

