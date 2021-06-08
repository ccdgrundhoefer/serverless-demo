import os

from flask import Flask, request
import psycopg2

app = Flask(__name__)

@app.route('/')
def empty():
   return 'API CREATE'

@app.route('/create', methods=['GET'])
def create_value():
   error = None

   if request.method == 'GET':
      if request.args.get('temp', ''):

         db = os.environ.get('DB')
         dbuser = os.environ.get('DBUSER')
         dbpassword = os.environ.get('DBPASS')
         dbhost = os.environ.get('DBHOST')

         temperature = request.args.get('temp', '')
         try:
            temp = float(temperature)

            db = os.environ.get('DB')
            dbuser = os.environ.get('DBUSER')
            dbpassword = os.environ.get('DBPASS')
            dbhost = os.environ.get('DBHOST')

            commands = """INSERT INTO temperature(value) VALUES(%f.2) RETURNING id"""
            
            try:
               # connect to the PostgreSQL server
               conn = psycopg2.connect(
                  host = dbhost,
                  database = db,
                  user = dbuser,
                  password = dbpassword
               )

               cur = conn.cursor()

               cur.execute(commands, (temperature,))
               id = cur.fetchone()[0]

               # commit the changes
               conn.commit()
               # close communication with the PostgreSQL database server
               cur.close()


               return "Database initialized"
            except (Exception, psycopg2.DatabaseError) as error:
               return error
            finally:
               if conn is not None:
                  conn.close()
         except ValueError:
            return "Invalid temperature"


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
         datetime TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
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
      
      # commit the changes
      conn.commit()
      # close communication with the PostgreSQL database server
      cur.close()

      return "Database initialized"
   except (Exception, psycopg2.DatabaseError) as error:
      return error
   finally:
      if conn is not None:
         conn.close()

if __name__ == "__main__":
   app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))