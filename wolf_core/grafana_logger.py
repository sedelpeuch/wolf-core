#! /usr/bin/env python3
import datetime
import threading

import mysql.connector


class GrafanaLogger():

    def __init__(self, logger=None):
        self.__dbName = "wolf"
        self.__tableName = "wolf_runner"
        self.__db = None
        self.__logger = logger
        self.__database_schema = ("id INT AUTO_INCREMENT PRIMARY KEY, time TIMESTAMP, job VARCHAR(255), "
                                  "status INT, message VARCHAR(255)")
        self.__create_use_db()
        self.post_lock = threading.Lock()

    def __create_use_db(self):
        """
        Try to create the database with the name of the class variable dbName.
        If it already exists, use it.
        and set the cursor.

        :return: None
        """
        self.__db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
        )
        self.__cursor = self.__db.cursor()
        try:  # Add if not exist
            self.__logger.warning("Creating database " + self.__dbName)
            self.__cursor.execute("CREATE DATABASE " + self.__dbName)
        except Exception as e:
            self.__logger.info("Could not create database: " + str(e))
        self.__db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database=self.__dbName
        )
        self.__cursor = self.__db.cursor()
        try:  # Drop if exist
            self.__logger.warning("Dropping table " + self.__tableName)
            self.__cursor.execute("DROP TABLE " + self.__tableName)
        except Exception as e:
            self.__logger.info("Could not drop table: " + str(e))
        self.__cursor.execute(
            "CREATE TABLE " + self.__tableName + " (" + self.__database_schema + ")")

    def post(self, job, status, message):
        """
        Post a message to the database.

        :param job: The job name.
        :param status: The status of the job.
        :param message: The message of the job.
        :return: None
        """
        sql = "INSERT INTO " + self.__tableName + " (time, job, status, message) VALUES (%s, %s, %s, %s)"
        val = (datetime.datetime.now(), job, status, message)
        self.post_lock.acquire()
        self.__cursor.execute(sql, val)
        self.__db.commit()
        self.post_lock.release()
