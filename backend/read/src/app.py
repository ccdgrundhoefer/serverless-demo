import os

from flask import Flask, request
import psycopg2

app = Flask(__name__)

@app.route('/', methods=['GET'])
def create_value():
   error = None

   if request.method == 'GET':

      db = os.environ.get('DB')
      dbuser = os.environ.get('DBUSER')
      dbpassword = os.environ.get('DBPASS')
      dbhost = os.environ.get('DBHOST')

      if request.args.get('time', ''):

         time = request.args.get('time', '')

         commands = """SELECT value FROM temperature order by id desc limit 1"""
      else:
         commands = """SELECT value FROM temperature order by id desc limit 1"""      

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
         temperature = cur.fetchone()

         # commit the changes
         conn.commit()
         # close communication with the PostgreSQL database server
         cur.close()

         return str(temperature)
      except (Exception, psycopg2.DatabaseError) as error:
         return error
      finally:
         if conn is not None:
            conn.close()
if __name__ == "__main__":
   app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))