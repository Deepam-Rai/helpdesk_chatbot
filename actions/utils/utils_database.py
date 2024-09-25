import psycopg2
from psycopg2 import extras
import logging
import os
from actions.utils.utils_environment import *
from actions.constants import *
from actions.constants_database import *
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
if db_connection:
    db_connection.set_session(autocommit=True)


def reconnect():
    """
    Called when db_connection needed to be reconnected
    """
    global db_connection
    db_connection = connect(DB_CONNECT_PARAMS)
    db_connection.set_session(autocommit=True)
    logger.debug("Reconnected db_connection.")


def insert_row(
        table_name: str,
        data: dict,
        schema: str,
        returning_id: str = None
        ):
    """
    Insert data into table based on condition
    Returns (true, row_id) if data was inserted else (false, error)
    parameters: {
        table_name: name of the table where the given data is to be inserted
        data: data to be inserted
        schema: the schema where the table exists
        returning_id: a parameter which specifies which column name to return as the unique id. Default: None
    }
    """
    logger.debug(f"table_name: {table_name}\n" f"insert-data: {data}")
    cursor = db_connection.cursor()
    try:
        keys = data.keys()
        columns = ",".join(keys)
        values_placeholders = ",".join(["%s" for _ in keys])
        values = [data[k] for k in keys]
        if returning_id:
            query = f'INSERT INTO "{schema}"."{table_name}" ({columns}) VALUES ({values_placeholders}) RETURNING "{returning_id}";'
        else:
            query = f'INSERT INTO "{schema}"."{table_name}" ({columns}) VALUES ({values_placeholders});'
        # query_string = cursor.mogrify(query, values)
        cursor.execute(query, values)

    except (psycopg2.OperationalError, psycopg2.InterfaceError) as error:
        logger.error("Error: %s" % error)
        logger.error("db_connection has closed unexpectedly. Reconnecting...")
        reconnect()
        logger.debug("Retrying the operation.")
        return insert_row(table_name, data, schema)
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error("Error: %s" % error)
        cursor.execute("rollback")
        cursor.close()
        return {False, f"ERROR: {error}"}
    row_count = cursor.rowcount
    fetch_id = None if returning_id is None else cursor.fetchone()[0]
    cursor.close()
    return (True, fetch_id) if row_count > 0 else (False, None)
