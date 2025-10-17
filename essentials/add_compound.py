from sqlite3 import connect
from parser import parser

# Add compounds to the db with their parsed formula
def add_compound():
  conn = connect('atomix.db')
  cursor = conn.cursor()

  formulae = []
  while True:
    formula = input('Enter formula (q to quit): ')
    if formula.lower() == 'q': break
    iupac = input('IUPAC Name: ')

    formulae.append((parser(formula), iupac))

  if formulae == []:
    raise ValueError('No formulae added.')

  cursor.executemany(f'''
    INSERT INTO compounds (formula, iupac)
    VALUES ({('?,'*len(formulae))[:-1]})
  ''', formulae)

  conn.commit()
  conn.close()

if __name__ == '__main__':
  add_compound()
