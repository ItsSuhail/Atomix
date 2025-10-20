from sqlite3 import connect, IntegrityError
from parse import parser

# Add compounds to the db with their parsed formula
def add_compound():
  # Establish db connection
  conn = connect('atomix.db')
  cursor = conn.cursor()

  while True:
    formula = input('Enter formula (q to quit): ')
    if formula.lower() == 'q': break # Exit case

    try:
      parsed = parser(formula)

      cursor.execute(f'''
        INSERT INTO compounds (formula)
        VALUES (?);
      ''', [parsed])

    except IntegrityError: # Throws exception if compound already exists
      print('Compound already added.')

    # For any other exception, commit and close to save progress and prevent memory leak
    except Exception as e:
      conn.commit()
      conn.close()
      raise e

    print()


  conn.commit()
  conn.close()

if __name__ == '__main__':
  add_compound()
