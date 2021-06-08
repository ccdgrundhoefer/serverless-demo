import os

from flask import Flask
import psycopg2

app = Flask(__name__)

@app.route('/')
def hello_world():
   target = os.environ.get('TARGET', 'World')
   return 'Hello {}!\n'.format(target)

@app.route('/initdb')
def create_tables():

   db = os.environ.get('DB')
   dbuser = os.environ.get('DBUSER')
   dbpassword = os.environ.get('DBPASS')
   dbhost = os.environ.get('DBHOST')

   commands = (
      """
      CREATE TABLE temperature (
         id SERIAL PRIMARY KEY,
         value decimal(255) NOT NULL
         datetime timestamp
      )
      """)
   
   try:
      # connect to the PostgreSQL server
      conn = psycopg2.connect(
         host = dbhost,
         database = db,
         user = dbuser,
         password = dbpassword
      )
      
      cur = conn.cursor()
      # create table one by one
      for command in commands:
         cur.execute(command)
      # close communication with the PostgreSQL database server
      cur.close()
      # commit the changes
      conn.commit()
   except (Exception, psycopg2.DatabaseError) as error:
      print(error)
   finally:
      if conn is not None:
         conn.close()

if __name__ == "__main__":
   app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))