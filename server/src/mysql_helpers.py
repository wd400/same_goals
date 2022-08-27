import pymysql
from pymysql.constants import CLIENT

import sys
from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PWD, MYSQL_DB
from logs import LOGGER

MILVUS_TABLE="milvus"

USERS_TABLE="users"

class MySQLHelper():
    """
      class
    """
    def __init__(self):
        self.conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, port=MYSQL_PORT, password=MYSQL_PWD,
                                    database=MYSQL_DB,
                                    local_infile=True,
                                     client_flag= CLIENT.MULTI_STATEMENTS)

        self.cursor = self.conn.cursor()
    #    self.cursor.execute("CREATE DATABASE IF NOT EXISTS DB;")
        #

     #   self.cursor.execute("USE DB;")
        
        self.create_mysql_tables()
        print("iiiiiiinit MySQLHelper done")

    def test_connection(self):
        print("TEST PING")
        try:
            self.conn.ping()
          #  self.cursor.execute("USE DB;")
            print("PING OK!")
        except Exception:
            print("PING FAIL")
            self.conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, port=MYSQL_PORT, password=MYSQL_PWD,
                                    database=MYSQL_DB,local_infile=True)
            self.cursor = self.conn.cursor()
            print("NEW CONN")

    def login(self, user,password):
        # Create mysql table if not exists
        self.test_connection()
        sql="SELECT EXISTS(SELECT * from "+USERS_TABLE+ " WHERE user=%s and password=%s);"
     
        try:
            self.cursor.execute(sql,(user,password))
            result=self.cursor.fetchone()
            print("RESULT",result)
            if result[0]==1:
                return True
            return False

        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            sys.exit(1)

    def signup(self, user,password):
        # Batch insert (Milvus_ids, img_path) to mysql
        print("bbbbbbbb")
        self.test_connection()
        print("aaaaaaa")
        sql = "insert into " + USERS_TABLE + " (user,password) values (%s,%s);"
        try:
            print("dans signup")
            self.cursor.execute(sql, (user,password))
            self.conn.commit()
            LOGGER.debug(f"New user added successfully")
            return True
        except pymysql.err.IntegrityError as e:
            return False
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")

            sys.exit(1)


    def count(self, user):
        # Get the number of mysql table
        self.test_connection()
        sql = "select count(milvus_id) from " + MILVUS_TABLE + " where user=%s;"
        try:
            self.cursor.execute(sql,(user,))
            results = self.cursor.fetchone()
            return results[0]
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            sys.exit(1)

    def add(self, user,todo):
        # Get the number of mysql table
        self.test_connection()
        sql = "select count(milvus_id) from " + MILVUS_TABLE + " where user=%s;"
        try:
            self.cursor.execute(sql,(user,))
            results = self.cursor.fetchone()
            if results[0]>=100:
                return False
            sql = "insert into " + MILVUS_TABLE + " (milvus_id,title,text) values (%s,%s,%s);"

            self.cursor.execute(sql, (user,todo))
            self.conn.commit()
                

        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            sys.exit(1)

    def update_description(self, user,description):
        # Get the number of mysql table
        print("user description",user,description)
        self.test_connection()
        sql = "update " + USERS_TABLE + " set description = %s where user=%s;"
        try:
            self.cursor.execute(sql,(description,user))
            self.conn.commit()
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            sys.exit(1)

    def id2user(self,id):
        # Get the number of mysql table
        self.test_connection()
        sql = "select user from " + MILVUS_TABLE + " where milvus_id=%s;"
        try:
            self.cursor.execute(sql,(id,))
            results = self.cursor.fetchone()
            return results[0]
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            sys.exit(1)

    def id2infos(self,id):
        # Get the number of mysql table
        self.test_connection()
        sql = "select user,todo from " + MILVUS_TABLE + " where milvus_id=%s;"
        try:
            self.cursor.execute(sql,(id,))
            results = self.cursor.fetchone()
            print('results',results)
            return results
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            sys.exit(1)

#add
#delete
#get
#modify description
#similar peoples
#similar golals

    def create_mysql_tables(self):
        # Create mysql table if not exists
        self.test_connection()
        sql1 = "create table if not exists " + MILVUS_TABLE + "(milvus_id BIGINT PRIMARY KEY, user VARCHAR(10) ,todo VARCHAR(100), INDEX (user));"
        sql2 = "create table if not exists " + USERS_TABLE + "(user VARCHAR(10) PRIMARY KEY, password VARCHAR(20) ,description VARCHAR(200));"
        try:
            LOGGER.error(f"BEFORE EXEC")
            self.cursor.execute(sql1)
            self.cursor.execute(sql2)
            self.conn.commit()
            LOGGER.debug(f"MYSQL create table: { MILVUS_TABLE} and {USERS_TABLE}  with sql")
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql")
            sys.exit(1)

    def load_data_to_mysql(self, id, user,todo):
        # Batch insert (Milvus_ids, img_path) to mysql
        self.test_connection()
        sql = "insert into " + MILVUS_TABLE + " (milvus_id,user,todo) values (%s,%s,%s);"
        try:
            self.cursor.execute(sql, (id,user,todo))
            self.conn.commit()
            
            LOGGER.debug(f"MYSQL loads data to table")
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            sys.exit(1)

    def user_ids(self,user):
        self.test_connection()
        sql="select milvus_id from "+MILVUS_TABLE+" where user=%s"
        try:
            self.cursor.execute(sql, (user,))
            results = self.cursor.fetchall()
            return [result[0] for result in results]
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e } with sql: {sql}")
            sys.exit(1)
       


    def user_todos(self,user):
        self.test_connection()
        sql="select milvus_id,todo from "+MILVUS_TABLE+" where user=%s"
        try:
            self.cursor.execute(sql, (user,))
            results = self.cursor.fetchall()
            print(results)
            array=[]
            for res in results:
                array.append(
                    {
                        "id":str(res[0]),
                        "todo":res[1]
                    }
                )
            return array
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e } with sql: {sql}")
            sys.exit(1)
       
    def get_description(self,user):
        self.test_connection()
        sql="select description from "+USERS_TABLE+" where user=%s"
        try:
            self.cursor.execute(sql, (user,))
            results = self.cursor.fetchone()
            print("DESCRIPTION RESULT",results)
            return results[0]
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e } with sql: {sql}")
            sys.exit(1)


    def search_by_milvus_ids(self, ids, table_name):
        # Get the img_path according to the milvus ids
        self.test_connection()
        str_ids = str(ids).replace('[', '').replace(']', '')
        sql = "select * from " + table_name + " where milvus_id in (" + str_ids + ") order by field (milvus_id," + str_ids + ");"
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            results_id = [res[0] for res in results]
            results_title = [res[1] for res in results]
            results_text = [res[2] for res in results]
            LOGGER.debug("MYSQL search by milvus id.")
            return results_id,results_title, results_text
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e } with sql: {sql}")
            sys.exit(1)

    def delete_table(self, id,user):
        # Delete mysql table if exists
        self.test_connection()
        sql = "delete from "+MILVUS_TABLE+" where milvus_id=%s and user=%s;"
        try:
            self.cursor.execute(sql,(id,user))
            self.conn.commit()
            if self.cursor.rowcount>0:
                return True
            return False


        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            sys.exit(1)

    def delete_all_data(self, table_name):
        # Delete all the data in mysql table
        self.test_connection()
        sql = 'delete from ' + table_name + ';'
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            LOGGER.debug(f"MYSQL delete all data in table:{table_name}")
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            sys.exit(1)


    def count(self, user):
        # Get the number of mysql table
        self.test_connection()
        sql = "select count(milvus_id) from " + MILVUS_TABLE + " where user=%s;"
        try:
            self.cursor.execute(sql,(user,))
            results = self.cursor.fetchone()
            return results
        except Exception as e:
            LOGGER.error(f"MYSQL ERROR: {e} with sql: {sql}")
            sys.exit(1)

