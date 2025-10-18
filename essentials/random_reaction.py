from sqlite3 import connect

def random_reaction():
  """
    Fetches a random reaction

    Returns:
      dict: products, reactants and unblankables
  """
  conn = connect('atomix.db')
  cursor = conn.cursor()

  cursor.execute('SELECT id FROM reactions ORDER BY random() LIMIT 1')
  reaction_id = cursor.fetchone()[0]

  # Join to get formula to return
  cursor.execute('''
    SELECT * FROM reaction_compounds JOIN compounds on compounds.id = compound_id WHERE reaction_id = ?
  ''', [reaction_id])
  compounds = cursor.fetchall();
  
  reactants, products, unblankables = [], [], []
  for ind, compound in enumerate(compounds):
    formula = compound[5]
    if compound[3] == 'product':
      products.append(formula)
    
    elif compound[3] == 'reactant':
      reactants.append(formula)

    if compound[2] == 0: unblankables.append(formula)
  

  conn.close()
  return { "products": products, "reactants": reactants, "unblankables": unblankables }


if __name__ == '__main__':
  random_reaction()
