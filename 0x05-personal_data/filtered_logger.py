#!/usr/bin/env python3
""" Module docstring """
# imports
import logging
import mysql.connector
from os import getenv
import re
from typing import List

PII_FIELDS = ("email", "phone", "ssn", "ip", "password")


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """ Returns the log message obfuscated """
    for field in fields:
        message = re.sub(
            f"{field}=(.+?){separator}",
            f"{field}={redaction}{separator}",
            message
        )
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter Class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Constructor """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.__fields = [i for i in fields]

    def format(self, record: logging.LogRecord) -> str:
        """ filter values in incoming log records """
        return filter_datum(
            self.__fields,
            self.REDACTION,
            super().format(record),
            self.SEPARATOR
        )


def get_logger() -> logging.Logger:
    """ Creates log for user data """
    user_data = logging.getLogger('user_data')
    user_data.setLevel(logging.INFO)
    user_data.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    user_data.addHandler(handler)
    return user_data


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Return a connection to a MySQL server """
    # mysql_login = {
    #     'user': getenv('HOLB_USERNAME'),
    #     'password': getenv('HOLB_PASSWORD'),
    #     'host': getenv('HOLB_DB_HOST'),
    #     'database': getenv('HOLB_DB_NAME')
    # }
    mysql_login = {
        'user': getenv('PERSONAL_DATA_DB_USERNAME'),
        'password': getenv('PERSONAL_DATA_DB_PASSWORD'),
        'host': getenv('PERSONAL_DATA_DB_HOST'),
        'database': getenv('PERSONAL_DATA_DB_NAME')
    }
    connection = mysql.connector.connect(**mysql_login)

    return connection


def main():
    """ Executes Log of current database """
    user_data = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for row in cursor:
        msg = "; ".join([f"{fields[i]}={str(col)}" for i, col in enumerate(row)])
        record = logging.LogRecord(user_data.name, logging.INFO, None, None, msg, None, None)
        user_data.handle(record)
    cursor.close()
    db.close()


if __name__ == "__main__":
    # print("Task 0:\n")
    # fields = ["password", "date_of_birth"]
    # messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;", "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]

    # for message in messages:
    #     print(filter_datum(fields, 'xxx', message, ';'))

    # print("\nTask 1:\n")
    # message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
    # log_record = logging.LogRecord("my_logger", logging.INFO, None, None, message, None, None)
    # formatter = RedactingFormatter(fields=("email", "ssn", "password"))
    # print(formatter.format(log_record))

    # print("\nTask 2:\n")
    # print(get_logger.__annotations__.get('return'))
    # print("PII_FIELDS: {}".format(len(PII_FIELDS)))

    # print("\nTask 3\n")
    # db = get_db()
    # cursor = db.cursor()
    # cursor.execute("SELECT COUNT(*) FROM users;")
    # for row in cursor:
    #     print(row[0])
    # cursor.close()
    # db.close()

    # print("\nTask 4\n")
    main()
