"""
vars: a, b, c etc.
and: .
or: +
xor: -
=: <->
"""


def count_vars(exp) -> int:
    
    """
    Função que retorna o número de variáveis existente numa expressão.
    exp: expressão a ser analizada.
    """

    az = 'abcdefghijklmnopqrstuvwxyz'

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

    """
    Função que retorna um dicionário que possui as colunas básicas (apenas as variáveis) de uma tabela verdade.
    """

    c_vars = count_vars(exp)

    # Define o número de linhas da tabela
    lines_count = 2**c_vars
    
    # Criação da lista "lines" que possui, ordenadamente, todas as linhas da tabela.
    lines = [binary(x, c_vars) for x in range(lines_count)]

    # Cria o dicionário das colunas
    letters = 'abcdefghijklmnopqrstuvwxyz'
    letters = letters[0:c_vars]
    cols = dict()
    for col in letters: cols[col] = list()

    # Pega os valores das linhas e transforma em formato de colunas
    for line in lines:
        for val, col  in zip(line, letters):
            cols[col].append(val)

    return cols


def main() -> None:

    """
    Código base, execução principal do programa.
    """

    # Entrada
    exp = input('Digite a expressão de tabela verdade: ')

    # Tratamento de entrada
    exp.replace(' ', '')
    exp.lower()

    # Define a tabela
    table = set_table(exp)
    


# Execução da base do programa
if __name__ == '__main__':
    main()
