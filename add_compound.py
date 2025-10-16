import mysql.connector as conn
from dotenv import load_dotenv
import os

load_dotenv()

mydb = conn.connect(
  host = os.getenv('DB_HOST'),
  user = os.getenv('DB_USER'),
  passwd = os.getenv('DB_PASS')
)

mycursor = mydb.cursor()
mycursor.execute('USE atomix')

def format_formula(s):
  # TODO: Format formula for storing in db
  return s

forms = ''
while True:
  s = input('Enter formula (q to quit): ')
  if s.lower() == 'q': break
  forms += ('("' + format_formula(s) + '"),')

forms = forms[:-1]

q_string = f'INSERT INTO compounds (formula) VALUES {forms}'
mycursor.execute(q_string)
mydb.commit()
