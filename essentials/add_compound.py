from sqlite3 import connect, IntegrityError
from parse import parser

# Add compounds to the db with their parsed formula
def add_compound():
  conn = connect('atomix.db')
  cursor = conn.cursor()

  while True:
    formula = input('Enter formula (q to quit): ')
    if formula.lower() == 'q': break
    # iupac = input('IUPAC Name: ')

    try:
      parsed = parser(formula)
      print(parsed)

      cursor.execute(f'''
        INSERT INTO compounds (formula)
        VALUES (?);
      ''', [parsed])

    except IntegrityError:
      print('Compound already added.')

    except Exception as e:
      conn.commit()
      conn.close()
      raise e

    print()


  conn.commit()
  conn.close()

if __name__ == '__main__':
  add_compound()
