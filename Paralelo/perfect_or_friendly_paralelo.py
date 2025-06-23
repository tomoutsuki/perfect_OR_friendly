import math
from typing import List, Tuple, Set, Dict
from collections import defaultdict
from threading import Thread
import time 
import queue
import csv


def calcular_soma_divisores(n: int) -> int:
    if n <= 1:
        return 0
    
    soma = 1  # 1 é sempre divisor próprio
    
    # Itera apenas até a raiz quadrada
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            soma += i
            # Adiciona o divisor correspondente, evitando duplicatas
            if i != n // i:
                soma += n // i
    
    return soma

def eh_numero_perfeito(n: int) -> bool:
    return n > 0 and calcular_soma_divisores(n) == n

def encontrar_numeros_perfeitos(limite: int) -> List[int]:
    perfeitos = []
    
    # Método otimizado usando primos de Mersenne para números pares
    def eh_primo(n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    # Verifica números perfeitos usando fórmula de Euclides
    p = 2
    while True:
        mersenne = (2 ** p) - 1
        if eh_primo(mersenne):
            perfeito = (2 ** (p - 1)) * mersenne
            if perfeito > limite:
                break
            perfeitos.append(perfeito)
        
        p += 1
        # Limite prático para evitar overflow
        if p > 50:
            break
    
    # Verifica números ímpares perfeitos por força bruta (muito raros)
    # Nota: Não se conhece nenhum número perfeito ímpar
    for n in range(1, min(limite + 1, 10000), 2):  # Limite menor para ímpares
        if eh_numero_perfeito(n):
            perfeitos.append(n)
    
    return sorted(perfeitos)

def sao_numeros_amigaveis(a: int, b: int) -> bool:
    return (a != b and 
            calcular_soma_divisores(a) == b and 
            calcular_soma_divisores(b) == a)

def encontrar_pares_amigaveis(limite: int) -> List[Tuple[int, int]]:
    pares_amigaveis = []
    soma_divisores_cache = {}
    
    def obter_soma_divisores(n):
        if n not in soma_divisores_cache:
            soma_divisores_cache[n] = calcular_soma_divisores(n)
        return soma_divisores_cache[n]
    
    verificados = set()
    
    for n in range(1, limite + 1):
        if n in verificados:
            continue
            
        soma_n = obter_soma_divisores(n)
        
        # Verifica se forma par amigável
        if soma_n != n and soma_n <= limite:
            soma_soma_n = obter_soma_divisores(soma_n)
            
            if soma_soma_n == n:
                # Encontrou par amigável
                par = tuple(sorted([n, soma_n]))
                if par not in pares_amigaveis:
                    pares_amigaveis.append(par)
                verificados.add(n)
                verificados.add(soma_n)
    
    return sorted(pares_amigaveis)


def processar_chunk_soma_divisores(chunk: List[int], resultado_queue: queue.Queue):
    resultados_chunk = {}
    for numero in chunk:
        resultados_chunk[numero] = calcular_soma_divisores(numero)
    
    resultado_queue.put(resultados_chunk)

def calcular_soma_divisores_paralelo(numeros: List[int], num_threads: int = 4) -> Dict[int, int]:
    if not numeros:
        return {}
    
    chunk_size = max(1, len(numeros) // num_threads)
    chunks = []
    
    for i in range(0, len(numeros), chunk_size):
        chunk = numeros[i:i + chunk_size]
        chunks.append(chunk)
    
    num_threads_efetivas = min(num_threads, len(chunks))
    
    resultado_queue = queue.Queue()
    threads = []
    
    for chunk in chunks:
        t = Thread(target=processar_chunk_soma_divisores, args=(chunk, resultado_queue))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    resultados_finais = {}
    while not resultado_queue.empty():
        chunk_resultado = resultado_queue.get()
        resultados_finais.update(chunk_resultado)
    
    return resultados_finais

def processar_chunk_amigaveis(inicio: int, fim: int, limite_global: int, resultado_queue: queue.Queue):
    pares_chunk = []
    soma_divisores_cache = {}
    
    def obter_soma_divisores(n):
        if n not in soma_divisores_cache:
            soma_divisores_cache[n] = calcular_soma_divisores(n)
        return soma_divisores_cache[n]
    
    verificados_locais = set()
    
    for n in range(inicio, fim + 1):
        if n in verificados_locais:
            continue
            
        soma_n = obter_soma_divisores(n)
        
        if soma_n != n and soma_n <= limite_global:
            soma_soma_n = obter_soma_divisores(soma_n)
            
            if soma_soma_n == n:
                par = tuple(sorted([n, soma_n]))
                pares_chunk.append(par)
                verificados_locais.add(n)
                verificados_locais.add(soma_n)
    
    resultado_queue.put(pares_chunk)

def encontrar_pares_amigaveis_paralelo(limite: int, num_threads: int = 4) -> List[Tuple[int, int]]:
    if limite <= 0:
        return []
    
    chunk_size = max(1, limite // num_threads)
    chunks = []
    
    for i in range(num_threads):
        inicio = i * chunk_size + 1
        fim = min((i + 1) * chunk_size, limite)
        
        if inicio <= limite:
            chunks.append((inicio, fim))
    
    num_threads_efetivas = min(num_threads, len(chunks))
    
    resultado_queue = queue.Queue()
    threads = []
    
    for inicio, fim in chunks:
        t = Thread(target=processar_chunk_amigaveis, 
                  args=(inicio, fim, limite, resultado_queue))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    todos_pares = []
    while not resultado_queue.empty():
        pares_chunk = resultado_queue.get()
        todos_pares.extend(pares_chunk)
    
    pares_unicos = list(set(todos_pares))
    return sorted(pares_unicos)

def processar_chunk_verificacao(numeros_chunk: List[int], resultado_queue: queue.Queue):
    resultados_chunk = []
    
    for n in numeros_chunk:
        soma_divisores = calcular_soma_divisores(n)
        eh_perfeito = eh_numero_perfeito(n)
        
        # Verifica se tem par amigável
        par_amigavel = None
        if soma_divisores != n and calcular_soma_divisores(soma_divisores) == n:
            par_amigavel = soma_divisores
        
        resultado = {
            'numero': n,
            'soma_divisores_proprios': soma_divisores,
            'eh_perfeito': eh_perfeito,
            'par_amigavel': par_amigavel,
            'eh_amigavel': par_amigavel is not None
        }
        
        resultados_chunk.append(resultado)
    
    resultado_queue.put(resultados_chunk)

def verificar_numeros_paralelo(numeros: List[int], num_threads: int = 4) -> List[Dict]:
    if not numeros:
        return []
    
    chunk_size = max(1, len(numeros) // num_threads)
    chunks = []
    
    for i in range(0, len(numeros), chunk_size):
        chunk = numeros[i:i + chunk_size]
        chunks.append(chunk)
    
    resultado_queue = queue.Queue()
    threads = []
    
    for chunk in chunks:
        t = Thread(target=processar_chunk_verificacao, args=(chunk, resultado_queue))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    todos_resultados = []
    while not resultado_queue.empty():
        chunk_resultado = resultado_queue.get()
        todos_resultados.extend(chunk_resultado)
    
    return todos_resultados

def analisar_intervalo_paralelo(inicio: int, fim: int, num_threads: int = 4) -> Dict:
    start_time = time.time()
    perfeitos = [n for n in encontrar_numeros_perfeitos(fim) if n >= inicio]
    todos_pares = encontrar_pares_amigaveis_paralelo(fim, num_threads)
    pares_no_intervalo = [
        par for par in todos_pares 
        if par[0] >= inicio or par[1] >= inicio
    ]
    
    end_time = time.time()
    
    return {
        'intervalo': (inicio, fim),
        'numeros_perfeitos': perfeitos,
        'pares_amigaveis': pares_no_intervalo,
        'total_perfeitos': len(perfeitos),
        'total_pares_amigaveis': len(pares_no_intervalo),
        'tempo_execucao': end_time - start_time,
        'threads_utilizadas': num_threads,
        'metodo': 'chunks'
    }

def verificar_numero_especifico(n: int) -> Dict:
    soma_divisores = calcular_soma_divisores(n)
    eh_perfeito = eh_numero_perfeito(n)
    
    par_amigavel = None
    if soma_divisores != n and calcular_soma_divisores(soma_divisores) == n:
        par_amigavel = soma_divisores
    
    return {
        'numero': n,
        'soma_divisores_proprios': soma_divisores,
        'eh_perfeito': eh_perfeito,
        'par_amigavel': par_amigavel,
        'eh_amigavel': par_amigavel is not None
    }

def salvar_csv(resultados, nome_arquivo=None):
    """Salva os resultados em um arquivo CSV"""
    if nome_arquivo is None:
        nome_arquivo = f"resultados_performance.csv"
    
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['intervalo', 'tempo_execucao']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for resultado in resultados:
            intervalo_tupla = resultado['intervalo']
            linha_csv = {
                'intervalo': f"{intervalo_tupla[0]}-{intervalo_tupla[1]}",  
                'tempo_execucao': resultado['tempo_execucao']
            }
            writer.writerow(linha_csv)

if __name__ == "__main__":
    numeros_teste = [1567, 8901, 34, 56789, 2345, 90, 7654, 123456, 987, 20000, 567, 8765, 12, 3456, 9876, 5432]
    resultados = verificar_numeros_paralelo(numeros_teste, num_threads=4)

    todos_resultados = []
    
    print("=== RESULTADOS PARALELOS ===")
    for resultado in resultados:
        print(f"Número {resultado['numero']}: "
              f"Perfeito={resultado['eh_perfeito']}, "
              f"Amigável={resultado['eh_amigavel']}")
    
    resultado_intervalo = analisar_intervalo_paralelo(1, 100000, num_threads=4)
    print(f"\nEncontrados no intervalo 1-100000:")
    print(f"  {resultado_intervalo['total_perfeitos']} números perfeitos")
    print(f"  {resultado_intervalo['total_pares_amigaveis']} pares amigáveis")
    print(f"  Tempo: {resultado_intervalo['tempo_execucao']:.3f}s")
    todos_resultados.append(resultado_intervalo)

    resultado_intervalo2 = analisar_intervalo_paralelo(1, 250000, num_threads=4)
    print(f"\nEncontrados no intervalo 1-250000:")
    print(f"  {resultado_intervalo2['total_perfeitos']} números perfeitos")
    print(f"  {resultado_intervalo2['total_pares_amigaveis']} pares amigáveis")
    print(f"  Tempo: {resultado_intervalo2['tempo_execucao']:.3f}s")
    todos_resultados.append(resultado_intervalo2)

    resultado_intervalo3 = analisar_intervalo_paralelo(1, 500000, num_threads=4)
    print(f"\nEncontrados no intervalo 1-500000:")
    print(f"  {resultado_intervalo3['total_perfeitos']} números perfeitos")
    print(f"  {resultado_intervalo3['total_pares_amigaveis']} pares amigáveis")
    print(f"  Tempo: {resultado_intervalo3['tempo_execucao']:.3f}s")
    todos_resultados.append(resultado_intervalo3)

    resultado_intervalo4 = analisar_intervalo_paralelo(1, 750000, num_threads=4)
    print(f"\nEncontrados no intervalo 1-750000:")
    print(f"  {resultado_intervalo4['total_perfeitos']} números perfeitos")
    print(f"  {resultado_intervalo4['total_pares_amigaveis']} pares amigáveis")
    print(f"  Tempo: {resultado_intervalo4['tempo_execucao']:.3f}s")
    todos_resultados.append(resultado_intervalo4)

    resultado_intervalo5 = analisar_intervalo_paralelo(1, 1000000, num_threads=4)
    print(f"\nEncontrados no intervalo 1-1000000:")
    print(f"  {resultado_intervalo5['total_perfeitos']} números perfeitos")
    print(f"  {resultado_intervalo5['total_pares_amigaveis']} pares amigáveis")
    print(f"  Tempo: {resultado_intervalo5['tempo_execucao']:.3f}s")
    todos_resultados.append(resultado_intervalo5)

    salvar_csv(todos_resultados)