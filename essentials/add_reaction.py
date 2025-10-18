from sqlite3 import connect, IntegrityError
from parser import parser

def add_reaction():
  conn = connect('atomix.db')
  cursor = conn.cursor()

  while True:
    if input('Another one? (y/n): ').lower() == 'n': break

    cursor.execute('''
      INSERT INTO reactions DEFAULT VALUES;
    ''')

    cursor.execute('''
      SELECT id FROM reactions ORDER BY id DESC LIMIT 1;
    ''')

    reaction_id = cursor.fetchone()[0]

    # REACTANTS
    print('Add reactants (q to stop)')
    cnt = 1
    while True:
      
      r = input(f'{cnt}: ')
      if r.lower() == 'q': break

      cnt += 1
      blankable = input('blankable? (default: y): ').lower()
      try:
        cursor.execute('INSERT INTO compounds (formula) VALUES (?)', [parser(r)])
        print('compound added\n')
      except IntegrityError: pass

      cursor.execute('''
        INSERT INTO reaction_compounds (reaction_id, compound_id, blankable, compound_type) VALUES (?, (SELECT id FROM compounds WHERE formula = ?), ?, ?)             
      ''', [reaction_id, parser(r), 0 if blankable == 'n' else 1, 'reactant'])

    # REACTANTS
    print('Add products (q to stop)')
    cnt = 1
    while True:
      
      r = input(f'{cnt}: ')
      if r.lower() == 'q': break

      cnt += 1
      blankable = input('blankable? (default: y): ').lower()
      try:
        cursor.execute('INSERT INTO compounds (formula) VALUES (?)', [parser(r)])
        print('compound added\n')
      except IntegrityError: pass

      cursor.execute('''
        INSERT INTO reaction_compounds (reaction_id, compound_id, blankable, compound_type) VALUES (?, (SELECT id FROM compounds WHERE formula = ?), ?, ?)             
      ''', [reaction_id, parser(r), 0 if blankable == 'n' else 1, 'product'])

      conn.commit()
  conn.close()

if __name__ == '__main__':
  add_reaction()
