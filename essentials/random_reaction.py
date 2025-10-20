from sqlite3 import connect
from essentials.parse import unparser
import random

def random_reaction(grade):
  """
    Fetches a random reaction of the given grade

    Args:
      grade: Reactions from which grade (11/12/C)

    Returns:
      dict: products, reactants and unblankables
  """
  if grade == 'C':
    grade = random.choice([11,12])

  # Establish db connection
  conn = connect('atomix.db')
  cursor = conn.cursor()

  # Fetch 1 reaction of 'grade' randomly
  cursor.execute(f'SELECT id FROM reactions WHERE grade = {grade} ORDER BY random() LIMIT 1')
  reaction_id = cursor.fetchone()[0]

  # Join to get formula to return
  cursor.execute('''
    SELECT * FROM reaction_compounds JOIN compounds on compounds.id = compound_id WHERE reaction_id = ?
  ''', [reaction_id])
  compounds = cursor.fetchall();
  
  reactants, products, unblankables, ele_symbols, ele_ids = [], [], [], set(), set()

  for ind, compound in enumerate(compounds):
    formula = compound[5]

    if compound[3] == 'product':
      products.append(formula)
    
    elif compound[3] == 'reactant':
      reactants.append(formula)

    if compound[2] == 0: unblankables.append(formula)

    unparsed = unparser(formula)
    ele_symbols = ele_symbols.union(set(unparsed[1]))
    ele_ids = ele_ids.union(set(unparsed[2]))
 

  conn.close()
  to_ret =  {
    'products': products,
    'reactants': reactants,
    'unblankables': unblankables,
    'ele_symbols': ele_symbols,
    'ele_ids': ele_ids
  }

  if __name__ == '__main__': print(to_ret)

  return to_ret


if __name__ == '__main__':
  random_reaction('12')
