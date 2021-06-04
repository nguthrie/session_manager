#!/usr/bin/python

import requests
import json
from config import config
import psycopg2

class SessionManager:

    test = None
    response = None
    ip_address = None
    session_id = None
    conn = None    

    def __init__(self, test):
        self.test=test

    def get_token(self):
        response = requests.get("https://jsonplaceholder.typicode.com/todos")
        self.response = response

    def parse_response(self):
        response_list = json.loads(self.response.text) 
        if self.test:
            self.ip_address, self.session_id = '111.222.333.444', 42
        else:
            self.ip_address, self.session_id = response_list[0]['userId'], response_list[0]['id'] 

    def update_database(self):
        """ Connect to the PostgreSQL database server """
        try:
            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**params)
            
            # create a cursor
            cur = self.conn.cursor()
            
        # execute a statement
            print('Inserting data into database:')
            sql = """INSERT INTO sessions(ip_address, session_id)
                VALUES (\'{}\', {})
                RETURNING id;""".format(self.ip_address, self.session_id)
            cur.execute(sql)

            # display the primary key of last inserted
            db_version = cur.fetchone()
            print(db_version)

            self.conn.commit()
        
        # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
                print('Database connection closed.')


if __name__ == '__main__':
    
    SM = SessionManager(True)
    SM.get_token()
    print(SM.response)
    SM.parse_response()
    print(SM.ip_address, SM.session_id)
    SM.update_database()

        