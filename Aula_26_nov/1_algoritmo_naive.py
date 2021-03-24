######################################################
#  Procura de padrões em sequências - Algoritmo 'naive'
#               Aula 26 Novembro
# Algoritmo que procura o padrão em todas as posições da sequência. 
# Este pode ser optimizado (através de algoritmos heurísticos, autómatos finitos, tries...).
########################################################


def procura_naive(seq, pattern):
    res = []
    for i in range(len(seq)-len(pattern)+1):                 # iteração sobre o comprimento da seq, tendo em conta o comprimento do padrao
        j = 0
        while j < len(pattern) and pattern[j]==seq[i+j]:     # j não pode ultrapassar comprimento do padrao; 
            j+=1                                             # se o primeiro caractere do padrao estiver no caracter seguinte da seq, avançar um no contador
        if j == len(pattern):                                # se j corresponder à posição final do padrão
            res.append(i)                                    # junta-se à lista de resultados a posição em que o padrão foi inicialmente encontrado na sequência
    return res

def teste():
    seq     = input('Sequence: ')
    pattern = input('Pattern: ') 
    pos     = procura_naive(seq, pattern)
    print('Pattern occurs in positions:', pos)

teste()
