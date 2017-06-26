"""
Description: Database Manager
Created : 08/04/2017
Modified : 08/04/2017
Started by: Julien Dcruz
Contributors: ...
"""


import sqlite3
import logging


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class dbmgr(object):
    
    errcode = None
    dbpath = None
    conn = None
    

    def __init__(self, db_path):
        self.dbpath = db_path
        #self.logger = logging.getLogger("log")


    def connect(self):
        try:
            self.conn = sqlite3.connect(self.dbpath)
        except sqlite3.OperationalError as err:
            print(err)
        
        
    def disconnect(self):
        self.conn.close()


    def run_insert_query(self, query, params):
        """
	    Description: Executes an insert sql query using Pythons DB-API (Parameter substitution)
	    Arguments: 'query': The sql query string
	               'params' : tuple containing parameters
	    """
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.OperationalError as msg:
            pass
            #self.logger.error(msg)
        except sqlite3.IntegrityError as msg:
            pass
            #self.logger.error('insert into database')
        return cursor.lastrowid
        

    def run_query(self, query, params):
        """
        Description: Executes an update/delete sql query using Pythons DB-API (Parameter substitution)
	    Arguments: query: The sql query string
	               'params' : tuple containing parameters
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.OperationalError as msg:
            pass
            #self.logger.error(msg)
        except sqlite3.IntegrityError as msg:
            pass
            #self.logger.warning(msg)


    def run_select_query(self, query, params=()):
        """
	    Description: Executes an select sql query using Pythons DB-API (Parameter substitution)
	    Arguments: 'query: The sql query string
	               'params' : tuple containing parameters
	    # Returns: False on failure | list[row_number][column_name] on success
        """
        self.conn.row_factory = dict_factory

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
        except sqlite3.OperationalError as msg:
            pass
            #self.logger.error(msg)

        data = cursor.fetchall()
        return data
