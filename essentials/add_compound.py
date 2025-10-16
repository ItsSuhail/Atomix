from supabase import create_client
from dotenv import load_dotenv
from parser import parser
from check_env import check_env
import os

load_dotenv()

@check_env
def add_compound():
  supabase = create_client(
    os.environ.get('DB_URL'), #type: ignore
    os.environ.get('DB_KEY')  #type: ignore
  )

  formulae = []
  while True:
    formula = input('Enter formula (q to quit): ')
    if formula.lower() == 'q': break
    iupac = input('IUPAC Name: ')

    formulae.append({
      'formula': parser(formula),
      'iupac': iupac
    })

  if formulae == []:
    raise ValueError('No formulae added.')

  response = (
    supabase.table('compounds')
      .insert(formulae)
      .execute()
  )

if __name__ == '__main__':
  add_compound()
