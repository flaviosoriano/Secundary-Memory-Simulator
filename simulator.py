import sys
import math

#===============================================================================
# Passagem dos argumentos via linha de comando
#===============================================================================
if len(sys.argv) > 4:
    tamanho_cache = int(sys.argv[1])
    tamanho_bloco = int(sys.argv[2])
    tamanho_conjuntos = int(sys.argv[3])
    arquivo = sys.argv[4]

    quantidade_linhas = int(tamanho_cache / tamanho_bloco)
    quantidade_conjuntos = int(quantidade_linhas / tamanho_conjuntos)
else:
    print("Informe os tamanhos da cache, bloco, conjunto e o arquivo de entrada.")
    sys.exit(1)

#===============================================================================
# Inicialização da cache
#===============================================================================
cache = [{'V': 0, 'tag': None} for _ in range(quantidade_linhas)]

#===============================================================================
# Leitura do arquivo de acessos à memória
#===============================================================================
array_de_acessos = []

try:
    with open(arquivo, 'r') as f:
        for linha in f:
            hexadecimal = linha.strip()
            if hexadecimal.startswith("0x"):
                hexadecimal = hexadecimal[2:]

            try:
                valor_decimal = int(hexadecimal, 16)
                valor_binario = format(valor_decimal, '032b')
                array_de_acessos.append(valor_binario)
            except ValueError:
                print(f"Erro ao converter a linha: {linha.strip()}")
except FileNotFoundError:
    print(f"Erro: O arquivo {arquivo} não foi encontrado.")
    sys.exit(1)

#===============================================================================
# Processamento dos acessos à memória
#===============================================================================
hits = 0
misses = 0

tags = []
indices_conjuntos = []

log_bloco = int(math.log2(tamanho_bloco))
log_conjuntos = int(math.log2(quantidade_conjuntos)) if quantidade_conjuntos > 1 else 0

for endereco_binario in array_de_acessos:
    # Remover os bits do offset do bloco
    tag_bin = endereco_binario[:-log_bloco] + '0' * log_bloco
    tags.append(tag_bin)

    # Determinar o índice do conjunto
    if quantidade_conjuntos > 1:
        indice_conjunto_bin = endereco_binario[-(log_bloco + log_conjuntos):-log_bloco]
        indice_conjunto = int(indice_conjunto_bin, 2)
    else:
        indice_conjunto = -1

    indices_conjuntos.append(indice_conjunto)

    # Converter a tag para hexadecimal
    tag_hex = format(int(tag_bin, 2), '08X')

    # Acesso à cache
    linha_inicial = indice_conjunto * tamanho_conjuntos if indice_conjunto != -1 else 0
    linha_final = linha_inicial + tamanho_conjuntos

    hit = False
    for i in range(linha_inicial, linha_final):
        if cache[i]['V'] == 1 and cache[i]['tag'] == tag_hex:
            hits += 1
            hit = True
            break

    if not hit:
        misses += 1
        for i in range(linha_inicial, linha_final):
            if cache[i]['V'] == 0:
                cache[i]['V'] = 1
                cache[i]['tag'] = tag_hex
                break

#===============================================================================
# Geração do arquivo de saída
#===============================================================================
with open("output.txt", 'w') as output:
    for i in range(quantidade_linhas):
        output.write(f"{i:03d} {cache[i]['V']} ")
        if cache[i]['V'] == 1:
            output.write(f"0x{cache[i]['tag']}\n")
        else:
            output.write("\n")
    
    output.write(f"#hits: {hits}\n")
    output.write(f"#miss: {misses}\n")

print("Simulação concluída. Resultados salvos em output.txt.")