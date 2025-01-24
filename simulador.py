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
cache = [{'V': 0, 'tag': None, 'idade': 0} for _ in range(quantidade_linhas)]

tempo_atual = 0  # Contador global de tempo para FIFO

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
                array_de_acessos.append(valor_decimal)
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

log_bloco = int(math.log2(tamanho_bloco))
log_conjuntos = int(math.log2(quantidade_conjuntos)) if quantidade_conjuntos > 1 else 0

with open("output.txt", 'w') as output:
    for endereco_decimal in array_de_acessos:
        tempo_atual += 1  # Incrementar o tempo a cada acesso
        
        # Remover os bits de deslocamento do bloco
        endereco_alinhado = endereco_decimal & ~(tamanho_bloco - 1)

        # Determinar o índice do conjunto se necessário
        if quantidade_conjuntos > 1:
            indice_conjunto = (endereco_alinhado // tamanho_bloco) % quantidade_conjuntos
        else:
            indice_conjunto = -1  # Cache totalmente associativa

        # Calcular a tag ignorando os bits de deslocamento e conjunto
        tag = endereco_alinhado >> (log_bloco + log_conjuntos)
        tag_hex = format(tag, '08X')

        linha_inicial = indice_conjunto * tamanho_conjuntos if indice_conjunto != -1 else 0
        linha_final = linha_inicial + tamanho_conjuntos

        # Verificar se há HIT na cache
        hit = False
        for i in range(linha_inicial, linha_final):
            if cache[i]['V'] == 1 and cache[i]['tag'] == tag_hex:
                hits += 1
                hit = True
                break

        if not hit:
            misses += 1
            substituido = False
            for i in range(linha_inicial, linha_final):
                if cache[i]['V'] == 0:
                    cache[i]['V'] = 1
                    cache[i]['tag'] = tag_hex
                    substituido = True
                    break

            if not substituido:
                # Implementação correta da política FIFO
                # Encontrar a linha mais antiga no conjunto
                linha_fifo = min(range(linha_inicial, linha_final), key=lambda x: cache[x]['idade'])
                cache[linha_fifo]['tag'] = tag_hex
                cache[linha_fifo]['idade'] = tempo_atual  # Atualizar com o novo tempo

        # Escrever o estado atual da cache no arquivo de saída
        output.write("================\n")
        output.write("IDX V ** ADDR **\n")
        for i in range(quantidade_linhas):
            output.write(f"{i:03d} {cache[i]['V']}")
            if cache[i]['V'] == 1:
                output.write(f" 0x{cache[i]['tag']}\n")
            else:
                output.write("\n")

    output.write("\n")
    output.write(f"#hits: {hits}\n")
    output.write(f"#miss: {misses}\n")

print("Simulação concluída. Resultados salvos em output.txt.")
