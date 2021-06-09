import os

from flask import Flask, request
import psycopg2

app = Flask(__name__)

@app.route('/')
def empty():
   return 'API CREATE'

@app.route('/create', methods=['POST'])
def create_value():
   error = None

   request_data = request.get_json()

   if request_data:
      temperature = request_data["temp"]
      humidity = request_data["humidity"]

      try:
         temp = str(temperature)

         db = os.environ['DB']
         dbuser = os.environ['DBUSER']
         dbpassword = os.environ['DBPASS']
         dbhost = os.environ['DBHOST']

         commands = """INSERT INTO temperature(value) VALUES(""" + temp + """) RETURNING id"""
         
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

            return "Added " + temp + " as id " + str(id)
         except (Exception, psycopg2.DatabaseError) as error:
            return str(error)
         finally:
            if conn is not None:
               conn.close()
      except ValueError:
         return "Invalid temperature"
   else:
      return str(request.get_json())


@app.route('/initdb')
def create_tables():

   db = os.environ['DB']
   dbuser = os.environ['DBUSER']
   dbpassword = os.environ['DBPASS']
   dbhost = os.environ['DBHOST']

   command = """
      CREATE TABLE temperature (
         id SERIAL PRIMARY KEY,
         value decimal(255) NOT NULL,
         datetime TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
      );
      """
   
   # connect to the PostgreSQL server
   conn = psycopg2.connect(
      host = dbhost,
      database = db,
      user = dbuser,
      password = dbpassword
   )

   cur = conn.cursor()

   cur.execute(command)
   
   # commit the changes
   conn.commit()
   # close communication with the PostgreSQL database server
   cur.close()

   return "Database initialized"

if __name__ == "__main__":
   app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))