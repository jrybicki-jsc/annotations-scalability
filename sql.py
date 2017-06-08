from functools import partial

import mysql.connector
from mysql.connector import errorcode
import os


def clean_db(connection):
    try:
        cursor = connection.cursor()
        cursor.execute('DROP TABLE `annotations`')
        cursor.execute('DROP DATABASE `annotests`')
    except:
        print 'Cleaning ended with some error'


def create_tables(connection):
    TABLES = {'annotations': (
        "CREATE TABLE `annotations` ("
        "  `body_id` varchar(32) NOT NULL,"
        "  `target_id` varchar(32) NOT NULL,"
        "  `created` date NOT NULL, "
        " PRIMARY KEY (body_id, target_id)"
        ") ENGINE=InnoDB")}

    cursor = connection.cursor()
    for name, stmt in TABLES.iteritems():
        try:
            cursor.execute(stmt)
        except:
            print 'Unable to create table'

    cursor.close()


def connect():
    host = os.getenv("MYSQL_PORT_3306_TCP_ADDR", "localhost")
    port = os.getenv("MYSQL_PORT_3306_TCP_PORT", "3306")
    password = os.getenv("MYSQL_ENV_MYSQL_ROOT_PASSWORD", "root")
    DB_NAME = 'annotests'

    cnx = mysql.connector.connect(user='root', password=password, host=host,
                                  port=port)
    cursor = cnx.cursor()

    try:

        cnx.database = DB_NAME
        cursor.execute('DROP TABLE `annotations`')

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(
                    DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    cnx.autocommit = True

    return cnx


class executor:
    def __enter__(self):
        self.connection = connect()
        create_tables(self.connection)
        store_function = partial(store_annotation, connection=self.connection)
        retrieve_function_1 = partial(retrieve_annotation_by_target,
                                      connection=self.connection)
        retrieve_function_2 = partial(retrieve_annotation_by_body,
                                      connection=self.connection)
        return store_function, retrieve_function_1, retrieve_function_2

    def __exit__(self, exc_type, exc_val, exc_tb):
        disconnect(self.connection)


def disconnect(connection):
    connection.close()


def store_annotation(annotation, connection):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO `annotations` (body_id, target_id, created) "
        "VALUES ("
        "   %(body_id)s, "
        "   %(target_id)s, "
        "   %(created)s"
        ")",
        {
            "body_id": annotation['body']['jsonld_id'],
            "target_id": annotation['target']['jsonld_id'],
            "created": annotation['created']
        })

    return cursor.fetchall()


def retrieve_annotation_by_target(target_id, connection):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM `annotations` "
        "WHERE `target_id`=%(id)s "
        "LIMIT 1",
        {'id': target_id}
    )

    return cursor.fetchall()


def retrieve_annotation_by_body(body_id, connection):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM `annotations` "
        "WHERE `body_id`=%(id)s "
        "LIMIT 1",
        {'id': body_id}
    )

    return cursor.fetchall()
