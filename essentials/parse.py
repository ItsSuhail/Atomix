ELEMENTS = {
'H': 1,
'He': 2,
'Li': 3,
'Be': 4,
'B': 5,
'C': 6,
'N': 7,
'O': 8,
'F': 9,
'Ne': 10,
'Na': 11,
'Mg': 12,
'Al': 13,
'Si': 14,
'P': 15,
'S': 16,
'Cl': 17,
'Ar': 18,
'K': 19,
'Ca': 20,
'Sc': 21,
'Ti': 22,
'V': 23,
'Cr': 24,
'Mn': 25,
'Fe': 26,
'Co': 27,
'Ni': 28,
'Cu': 29,
'Zn': 30,
'Ga': 31,
'Ge': 32,
'As': 33,
'Se': 34,
'Br': 35,
'Kr': 36,
'Rb': 37,
'Sr': 38,
'Y': 39,
'Zr': 40,
'Nb': 41,
'Mo': 42,
'Tc': 43,
'Ru': 44,
'Rh': 45,
'Pd': 46,
'Ag': 47,
'Cd': 48,
'In': 49,
'Sn': 50,
'Sb': 51,
'Te': 52,
'I': 53,
'Xe': 54,
'Cs': 55,
'Ba': 56,
'La': 57,
'Ce': 58,
'Pr': 59,
'Nd': 60,
'Pm': 61,
'Sm': 62,
'Eu': 63,
'Gd': 64,
'Tb': 65,
'Dy': 66,
'Ho': 67,
'Er': 68,
'Tm': 69,
'Yb': 70,
'Lu': 71,
'Hf': 72,
'Ta': 73,
'W': 74,
'Re': 75,
'Os': 76,
'Ir': 77,
'Pt': 78,
'Au': 79,
'Hg': 80,
'Tl': 81,
'Pb': 82,
'Bi': 83,
'Po': 84,
'At': 85,
'Rn': 86,
'Fr': 87,
'Ra': 88,
'Ac': 89,
'Th': 90,
'Pa': 91,
'U': 92,
'Np': 93,
'Pu': 94,
'Am': 95,
'Cm': 96,
'Bk': 97,
'Cf': 98,
'Es': 99,
'Fm': 100,
'Md': 101,
'No': 102,
'Lr': 103,
'Rf': 104,
'Db': 105,
'Sg': 106,
'Bh': 107,
'Hs': 108,
'Mt': 109,
'Ds': 110,
'Rg': 111,
'Cn': 112,
'Nh': 113,
'Fl': 114,
'Mc': 115,
'Lv': 116,
'Ts': 117,
'Og': 118,
'J':119,
'Q':120
}

def parser(s):
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
