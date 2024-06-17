"""
vars: a, b, c etc.
and: .
or: +
xor: -
=: <->

ordem:
1º: ()
2º: {}
3º: .
4º: +
5º: -
6º: =
"""

az = 'abcdefghijklmnopqrstuvwxyz'


def count_vars(exp) -> int:
    
    """
    Função que retorna o número de variáveis existente numa expressão.
    exp: expressão a ser analizada.
    """

    global az

    # O laço checa a primeira letra que não está na expressão; ao encontrar, retorna o index 
    for index, letter in enumerate(az):
        if letter not in exp:
            return index


def binary(num, c_dcm=1) -> str:
    
    """
    Retorna a versão binária de um 'int' com tratamentos:
    * Número de casas controlado;
    * Retorno em str sem o prefixo '0b'.

    num: número int a ser transformado
    c_dcm (opcional): número de casas mínimo que número deve ter
    """

    # Define a variável com o binário sem prefixo
    bi = bin(num)[2:]

    # Adciona as casas decimais em branco, se nescessário
    while len(bi) < c_dcm: bi = '0'+bi

    return bi


def set_table(exp) -> dict:

    global az

    """
    Função que retorna um dicionário que possui as colunas básicas (apenas as variáveis) de uma tabela verdade.
    """

    c_vars = count_vars(exp)

    # Define o número de linhas da tabela
    lines_count = 2**c_vars
    
    # Criação da lista "lines" que possui, ordenadamente, todas as linhas da tabela.
    lines = [binary(x, c_vars) for x in range(lines_count)]

    # Cria o dicionário das colunas
    letters = az[0:c_vars]
    cols = dict()
    for col in letters: cols[col] = list()

    # Pega os valores das linhas e transforma em formato de colunas
    for line in lines:
        for val, col  in zip(line, letters):
            cols[col].append(val)

    return cols


def op(col_1, col_2, op) -> list:

    """Função que retorna uma coluna resuldada de uma operação de duas colunas dadas em parâmetros."""

    rtn_col = list()

    if op == '.': # and
        for c1, c2 in zip(col_1, col_2):
            rtn_col.append('1') if (c1 == '1') and (c2 == '1') else rtn_col.append('0')

    elif op == '+': # or
        for c1, c2 in zip(col_1, col_2):
            rtn_col.append('1') if (c1 == '1') or (c2 == '1') else rtn_col.append('0')

    elif op == '-': # xor
        for c1, c2 in zip(col_1, col_2):
            rtn_col.append('1') if (c1 == '1') ^ (c2 == '1') else rtn_col.append('0')

    elif op == '=': # igual
        for c1, c2 in zip(col_1, col_2):
            rtn_col.append('1') if c1 == c2 else rtn_col.append('0')

    return rtn_col


def neg(col) -> list:
    
    """
    Função que retorna a versão negada de uma coluna.
    """

    rtn_col = list()

    for line in col:
        rtn_col.append('1') if line == '0' else rtn_col.append('0')

    return rtn_col


def is_col(table, col) -> bool:
    """
    Retorna se uma coluna está registrada.
    table = tabela total
    col = nome da coluna a ser checada.
    """

    return True if col in table.keys() else False


def is_op(op) -> bool:
    """
    Retorna se a expressão é uma operação.
    """ 

    return True if op.count('[') == 2 else False


def work_set(_open, _close, work_exp, cut_start, cut_end) -> None:

    '''
    Função que realiza a determinação do work_exp, limitando uma parte dele em () ou {}.
    Ex: ([a]+[b]).[c] -> [a]+[b]
    '''

    while work_exp.count(_open) != 0:
        p_open = 1
        for index, c in enumerate(work_exp[work_exp.find(_open)+1:]):
            if c == _open: p_open += 1
            elif c == _close: p_open -= 1
            if p_open == 0:
                cut_start = work_exp.find(_open)+1
                cut_end = index
                work_exp = work_exp[work_exp.find(_open)+1:index]
                break


def main() -> None:

    """
    Código base, execução principal do programa.
    """

    global az

    # Entrada
    exp = input('Digite a expressão de tabela verdade: ')

    # Tratamento de entrada
    exp.replace(' ', '')
    exp.lower()

    # Cria a variável com a expressão com as colunas definidas
    # Ex: a.b+c -> [a].[b]+[c]
    exp_ac = exp
    for letter in az:
        if letter in exp: 
            exp_ac = exp_ac.replace(letter, f'[{letter}]')
        else:
            break

    # Define a tabela
    table = set_table(exp)

    # While que segue a regra de criação de colunas da tabela verdade até concluir a operação
    while not is_col(table, f'[{exp}]'):
        work_exp = exp_ac
        cut_start = 0
        cut_end = len(work_exp)
        
        while True:
            if is_op(work_exp):
                break

            if '(' in work_exp:
                work_set('(', ')', work_exp, cut_start, cut_end)
            
            elif '{' in work_exp:
                work_set('{', '}', work_exp, cut_start, cut_end)
                if is_col(table, work_exp):
                    table['{'+work_exp+'}'] = neg(work_exp)
                    exp_ac = exp_ac[:cut_start]+'['+exp_ac[cut_start+1:cut_end]+']'+exp_ac[cut_end:]
                    break
            
            elif '.' in work_exp:
                pass

            elif '+' in work_exp:
                pass
            
            elif '-' in work_exp:
                pass

            elif '=' in work_exp:
                pass


# Execução da base do programa
if __name__ == '__main__':
    main()
