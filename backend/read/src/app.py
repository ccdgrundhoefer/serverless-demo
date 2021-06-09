import os

from flask import Flask, request
from flask_cors import CORS
import json
import psycopg2

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def read_latest():
   error = None

   db = os.environ.get('DB')
   dbuser = os.environ.get('DBUSER')
   dbpassword = os.environ.get('DBPASS')
   dbhost = os.environ.get('DBHOST')

   commands = """SELECT temperature, humidity, datetime FROM sensordata order by id desc limit 1"""      

   try:
      # connect to the PostgreSQL server
      conn = psycopg2.connect(
         host = dbhost,
         database = db,
         user = dbuser,
         password = dbpassword
      )

      cur = conn.cursor()
      cur.execute(commands)
      row = cur.fetchone()

      # commit the changes
      conn.commit()
      # close communication with the PostgreSQL database server
      cur.close()

      x = {
         "temperature": str(row[0]),
         "humidity": str(row[1]),
         "timestamp": str(row[2])
      }

      return json.dumps(x)
   except (Exception, psycopg2.DatabaseError) as error:
      return error
   finally:
      if conn is not None:
         conn.close()

@app.route('/chart', methods=['GET'])
def get_chart():
   error = None

   db = os.environ.get('DB')
   dbuser = os.environ.get('DBUSER')
   dbpassword = os.environ.get('DBPASS')
   dbhost = os.environ.get('DBHOST')

   commands = """SELECT temperature FROM sensordata order by id desc limit 10"""      

   try:
      # connect to the PostgreSQL server
      conn = psycopg2.connect(
         host = dbhost,
         database = db,
         user = dbuser,
         password = dbpassword
      )

      cur = conn.cursor()
      cur.execute(commands)
      row = cur.fetchone()

      res = []
      res.append(row[0])

      while row is not None:
         res.append(row[0])
         row = cur.fetchone() 

      # commit the changes
      conn.commit()
      # close communication with the PostgreSQL database server
      cur.close()

      app.logger.info(res)

      return json.dumps(res)
      
   except (Exception, psycopg2.DatabaseError) as error:
      return error
   finally:
      if conn is not None:
         conn.close()

if __name__ == "__main__":
   app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))