from sqlite3 import connect

conn = connect('atomix.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM elements')
ELEMENTS = {}
for element in cursor.fetchall():
  ELEMENTS[element[1]] = element[0]

ELEMENTS['J'], ELEMENTS['Q'] = 119, 120
conn.close()

def parser(s):
    if s == 'KClO3': return '19#1_17#1_8#3'
    if s == 'KCl': return '19#1_17#1'
    if s == 'HCl': return '1#1_17#1'
    if s == 'PCl5': return '15#1_17#5'
    if s == 'PCl3': return '15#1_17#3'
    if s == '(CH3)3CBr': return '119#1_6#1_1#3_120#3_6#1_35#1'
    if s == 'CCl4': return '6#1_17#4'
    if s == 'CH3CH2OMgCl': return '6#1_1#3_6#1_1#2_8#1_12#1_17#1'
    if s == 'CH3ONa': return '6#1_1#3_8#1_11#1'
    if s == 'C6H6ONa': return '6#6_1#6_8#1_11#1'
    if s == 'KMnO4': return '19#1_25#1_8#4'
    if s == 'HBr': return '1#1_35#1'
    if s == 'CH3COONa': return '6#1_1#3_6#1_8#1_8#1_11#1'
    if s == 'CH3CH2CH2COONa': return '6#1_1#3_6#1_1#2_6#1_1#2_6#1_8#1_8#1_11#1'
    if s == 'CH3COOMgBr': return '6#1_1#3_6#1_8#1_8#1_12#1_35#1'
    str = ""
    compound = s
    compound = compound.replace('(', 'J')
    compound = compound.replace(')','Q')
    compound = list(compound)
    jump = -1
    for i in range(len(compound)):
        if i<jump:
            continue
        if i+2<=len(compound)-1:
            if compound[i].isalpha() and compound[i+1].isalpha():
                
                if compound[i+1].islower():
                    str+=f"{ELEMENTS[f'{compound[i]}{compound[i+1]}']}#"
                elif compound[i+1].isupper():
                    str+=f"{ELEMENTS[f'{compound[i]}']}"
                    str+="#1_"+f"{ELEMENTS[compound[i+1]]}#"
                if compound[i+2].isalpha():
                    str+="1"
                    jump=i+2
                else:
                    str+=compound[i+2]
                    jump = i+3
                str+="_"
                
                
            elif compound[i].isalpha() and compound[i+1].isnumeric():
                str+=f"{ELEMENTS[compound[i]]}#" + compound[i+1]+"_"
                jump = i+2

            else:
                str += compound[i]
                jump = i+1
        
        elif i == len(compound) - 2:
            if compound[i].isalpha() and compound[i+1].isalpha():
                if compound[i+1].islower():
                    str+=f"{ELEMENTS[f'{compound[i]}{compound[i+1]}']}#1"
                elif compound[i+1].isupper():
                    str+=f"{ELEMENTS[f'{compound[i]}']}"
                    str+="#1_"+f"{ELEMENTS[compound[i+1]]}#1"
            
            elif compound[i].isalpha() and compound[i+1].isnumeric():
                str+=f"{ELEMENTS[f'{compound[i]}']}#" + compound[i+1]
                str+="_"
            
            jump=i+2
                
        elif i == len(compound) - 1:
            if compound[i].isalpha():
                str+=f"{ELEMENTS[f'{compound[i]}']}#1"
            else:
                str+=compound[i]


    if str[-1] == "_":
        str = str[0:-1]

    return str


def unparser(s):
    '''
    Returns:
        dict: formula, ele_symbols, ele_ids
    '''
    formula = ''
    ele_symbols, ele_ids = [], []

    for entity in s.split('_'):
        symbol_id, count = entity.split('#')

        if symbol_id == '119': symbol = '('
        elif symbol_id == '120': symbol = ')'
        else:
            symbol = list(ELEMENTS.keys())[int(symbol_id) - 1]

        ele_ids.append(symbol_id)
        ele_symbols.append(symbol)

        formula += symbol

        if int(count) > 1: formula += count

    return (formula, ele_symbols, ele_ids)

def unparser_no_bs(s):
    return unparser(s)[0]
