"""
LEGENDA:
vars: a, b, c etc.
negação: {}
and: .
or: +
xor: -
<->: =

ORDEM:
1º: ()
2º: {}
3º: .
4º: +
5º: -
6º: =
"""

az = 'abcdefghijklmnopqrstuvwxyz' # Variável que armazena o alfabeto


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


def op(op, table) -> list:

    """
    Função que retorna uma coluna resuldada de uma operação.
    op = Operação;
    table = Tabela de colunas;
    """

    col_1 = table[op[op.find('[')+1:op.find(']')]]
    act = op[op.find(']')+1]
    col_2 = op[op.find(']')+3:-1].replace(']', '')
    col_2 = col_2.replace('[', '')
    col_2 = table[col_2]

    rtn_col = list()

    if act == '.': # and
        for c1, c2 in zip(col_1, col_2):
            rtn_col.append('1') if (c1 == '1') and (c2 == '1') else rtn_col.append('0')

    elif act == '+': # or
        for c1, c2 in zip(col_1, col_2):
            rtn_col.append('1') if (c1 == '1') or (c2 == '1') else rtn_col.append('0')

    elif act == '-': # xor
        for c1, c2 in zip(col_1, col_2):
            rtn_col.append('1') if (c1 == '1') ^ (c2 == '1') else rtn_col.append('0')

    elif act == '=': # igual
        for c1, c2 in zip(col_1, col_2):
            rtn_col.append('1') if c1 == c2 else rtn_col.append('0')

    return rtn_col


def neg(col_name, table) -> list:
    
    """
    Função que retorna a versão negada de uma coluna.
    """

    col = table[col_name[1:-1]]
    rtn_col = list()
    
    for line in col:
        rtn_col.append('1') if line == '0' else rtn_col.append('0')

    return rtn_col


def is_col(table, col) -> bool:
    """
    Retorna se uma coluna está registrada.\n
    table = tabela total\n
    col = nome da coluna a ser checada.
    """

    col_filtro = col.replace('[', '')
    col_filtro = col_filtro.replace(']', '')

    return True if col_filtro in table.keys() else False


def is_op(op) -> bool:
    """
    Retorna se a expressão é uma operação.
    """ 

    return True if op.count('[') == 2 else False


def work_set(exp, cut_start, cut_end, _open, _close) -> tuple:

    '''
    Função que realiza a determinação da 'Área de trabalho' de uma expressão, limitando uma parte dele em () ou {}.
    Ex: ([a]+[b]).[c] -> [a]+[b]
    '''

    if exp.count(_open) > 0:
        start = exp[cut_start:cut_end].find(_open)+1
        p_open = 1

        for index, c in enumerate(exp[start:]):
            if c == _open: p_open += 1
            elif c == _close: p_open -= 1
            if p_open == 0:
                cut_start += start
                cut_end = start+index
                break

    return cut_start-1, cut_end+1


def has_op(op, exp) -> bool:

    """
    Retorna um valor bool referente a checagem de se há um operador expecífico (op) numa expressão ou trecho de expressão (exp).
    Filtra resultados dentro de colunas. 
    Exemplo: 
    * op = +, exp = [a+b].[c] -> False; 
    * op = ., exp = [a+b].[c] -> True.
    """

    ex = exp
    while ex.count('[') != 0:
        ex = ex.replace(ex[ex.find('['):ex.find(']')+1], '', 1)
    
    return True if ex.count(op) > 0 else False 


def set_op(exp_ac, cut_start, cut_end, op) -> tuple:

    """
    Retorna o cut_start e cut_end de uma 'área de trabalho' para ser apenas uma operação expecífica.
    Exemplo: op = ., exp_ac = [a]+[b].[c] -> [b].[c]
    """

    op_point = 0

    for index, c in enumerate(exp_ac[cut_start:cut_end]):
        if c == op and exp_ac[cut_start+index-1] == ']' and exp_ac[cut_start+index+1] == '[':
            op_point = cut_start+index
            cut_start = exp_ac.rfind('[', 0, op_point)
            cut_end = exp_ac.find(']', op_point)+1
            return cut_start, cut_end


def main() -> None:

    """
    Código base, execução principal do programa.
    """

    global az

    # Entrada
    exp = input('Digite a expressão de tabela verdade: ')

    # Tratamento de entrada
    exp = exp.replace(' ', '')
    exp = exp.lower()

    # Cópia da expressão que é alterada ao longo do processo de solução da expressão.
    exp_ac = exp

    # Define a tabela
    table = set_table(exp)

    # Remove os parênteses apenas da variável original da expressão para facilitar a checagem de quando a coluna resposta for criada.
    exp = exp.replace('(', '')
    exp = exp.replace(')', '')

    # Cria a variável com a expressão com as colunas definidas
    # Ex: a.b+c -> [a].[b]+[c]
    for letter in az:
        if letter in exp_ac: 
            exp_ac = exp_ac.replace(letter, f'[{letter}]')
        else:
            break

    # While que segue a regra de prioridades da tabela verdade para criar as colunas na ordem correta, assim, solucionando a operação.
    while not is_col(table, exp): # Enquanto a expressão não for uma coluna cadastrada na tabela, repete o laço.
        # Criação de variáveis que limitam a "Área de trabalho" da expressão (negações e parenteses).
        cut_start = 0
        cut_end = len(exp_ac)
        is_neg = False # Variável de controle usada posteriormente para checar se a operação atual é uma operação comum ou uma negação.
        
        # While que só encerra ao encontrar a primeira operação dentro da expressão, seguindo a ordem de prioridade.
        # Exemplo: [a]+[b].[c] -> op = [b].[c]
        while True:
            print(exp_ac, exp_ac[cut_start:cut_end])

            # Checa se o trecho atual da expressão já é uma operação e, se for, sai do laço. 
            if is_op(exp_ac[cut_start:cut_end]):
                break

            # Limita a "Área de trabalho" da expressão para dentro dos parênteses, se houver"
            if has_op('(', exp_ac[cut_start:cut_end]):
                cut_start, cut_end = work_set(exp_ac, cut_start, cut_end, '(', ')')
                if is_col(table, exp_ac[cut_start:cut_end]): # Se o conteúdo dos parênteses for apenas uma coluna, remove os mesmos.
                    exp_ac = exp_ac[:cut_start-1]+exp_ac[cut_start:cut_end]+exp_ac[cut_end+1:]
                    cut_start = 0
                    cut_end = len(exp_ac)
            
            # Limita a "Área de trabalho" da expressão para dentro das negações, se houver. Cria a coluna negada se possível."
            elif has_op('{', exp_ac[cut_start:cut_end]):
                # Se a "Área de trabalho" for uma coluna já cadastrada na tabela, cria a versão negada da coluna e sai do laço.
                if is_col(table, exp_ac[cut_start+1:cut_end-1]):
                    table['{'+exp_ac[cut_start+2:cut_end-2]+'}'] = neg(exp_ac[cut_start+1:cut_end-1], table)

                    is_neg = True
                    break

                cut_start, cut_end = work_set(exp_ac, cut_start, cut_end, '{', '}')
            
            # Se houver um AND na "Área de trabalho" da expressão, configura a operação para ser resolvida e sai do laço"
            elif has_op('.', exp_ac[cut_start:cut_end]):  
                cut_start, cut_end = set_op(exp_ac, cut_start, cut_end, '.')
                break

            # Se houver um OR na "Área de trabalho" da expressão, configura a operação para ser resolvida e sai do laço"
            elif has_op('+', exp_ac[cut_start:cut_end]):
                cut_start, cut_end = set_op(exp_ac, cut_start, cut_end, '+')
                break

            # Se houver um XOR na "Área de trabalho" da expressão, configura a operação para ser resolvida e sai do laço"
            elif has_op('-', exp_ac[cut_start:cut_end]):
                cut_start, cut_end = set_op(exp_ac, cut_start, cut_end, '-')
                break

            # Se houver um EQUAL na "Área de trabalho" da expressão, configura a operação para ser resolvida e sai do laço"
            elif has_op('=', exp_ac[cut_start:cut_end]):
                cut_start, cut_end = set_op(exp_ac, cut_start, cut_end, '=')
                break

        # Após definir a operação a ser feita, cria a coluna na tabela para a operação e atualiza o exp_ac.
        # Atualizar exp_ac: [a]-[b]+[c] -> [a]-[b+c] -> [a-b+c]. (Veja um exemplo mais desenvolvido em "logictest.txt")
        
        # Se a "Coluna resposta" já existir encerra o laço indo para a resposta.
        if is_col(table, exp_ac): break

        # Atualização em caso de negação
        if is_neg:
            temp = exp_ac[cut_start:cut_end]
            temp = temp.replace('{[', '[{', 1)
            temp = temp.replace(']}', '}]', 1)
            exp_ac = exp_ac[:cut_start]+temp+exp_ac[cut_end:]
            del temp
        
        # Atualização em caso de operação comum
        else:
            col_name = exp_ac[cut_start:cut_end]
            col_name = col_name.replace('[','')
            col_name = col_name.replace(']','')
            table[col_name] = op(exp_ac[cut_start:cut_end], table)
            exp_ac = exp_ac[:cut_start]+f'[{col_name}]'+exp_ac[cut_end:]

    # Quando o programa achar a resposta, imprime a coluna respota na tela
    print(table[exp])


# Execução da base do programa
if __name__ == '__main__':
    main()
