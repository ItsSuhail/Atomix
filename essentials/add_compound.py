import mysql.connector as conn
from dotenv import load_dotenv
from essentials.parser import parser
import os

load_dotenv()

mydb = conn.connect(
  host = os.getenv('DB_HOST'),
  user = os.getenv('DB_USER'),
  passwd = os.getenv('DB_PASS')
)

mycursor = mydb.cursor()
mycursor.execute('USE atomix')

forms = ''
while True:
  s = input('Enter formula (q to quit): ')
  if s.lower() == 'q': break
  forms += ('("' + parser(s) + '"),')

forms = forms[:-1]

q_string = f'INSERT INTO compounds (formula) VALUES {forms}'
mycursor.execute(q_string)
mydb.commit()
