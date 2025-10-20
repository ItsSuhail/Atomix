from sqlite3 import connect, IntegrityError
from parse import parser

def add_reaction():
  conn = connect('atomix.db')
  cursor = conn.cursor()

  # Per reaction
  while True:
    if input('Another one? (y/n): ').lower() == 'n': break

    # Create new reaction and get its ID
    cursor.execute('INSERT INTO reactions (grade) VALUES (\'11\')')
    cursor.execute('SELECT id FROM reactions ORDER BY id DESC LIMIT 1')
    reaction_id = cursor.fetchone()[0]

    # Per reactant
    print('Add reactants (q to stop)')
    cnt = 1
    while True:
      
      r = input(f'{cnt}: ')
      if r.lower() == 'q': break

      cnt += 1
      blankable = input('blankable? (default: y): ').lower()

      # Add compound to the db if not already added
      try:
        cursor.execute('INSERT INTO compounds (formula) VALUES (?)', [parser(r)])
        print('compound added\n')
      except IntegrityError: pass

      # Add compound to junction table
      cursor.execute('''
        INSERT INTO reaction_compounds (reaction_id, compound_id, blankable, compound_type)
        VALUES (?, (SELECT id FROM compounds WHERE formula = ?), ?, ?)             
      ''', [reaction_id, parser(r), 0 if blankable == 'n' else 1, 'reactant'])

    # Per product
    print('Add products (q to stop)')
    cnt = 1
    while True:
      
      r = input(f'{cnt}: ')
      if r.lower() == 'q': break

      cnt += 1
      blankable = input('blankable? (default: y): ').lower()

      # Add compound to the db if not already added
      try:
        cursor.execute('INSERT INTO compounds (formula) VALUES (?)', [parser(r)])
        print('compound added\n')
      except IntegrityError: pass

      # Add compound to junction table
      cursor.execute('''
        INSERT INTO reaction_compounds (reaction_id, compound_id, blankable, compound_type) VALUES (?, (SELECT id FROM compounds WHERE formula = ?), ?, ?)             
      ''', [reaction_id, parser(r), 0 if blankable == 'n' else 1, 'product'])

      # Commit after every reaction in case an error occurs with parsing to not lose progress
      conn.commit()

  conn.close()

if __name__ == '__main__':
  add_reaction()
