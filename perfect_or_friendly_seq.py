import math
from typing import List, Tuple, Set, Dict
from collections import defaultdict

def calcular_soma_divisores(n: int) -> int:
    """
    Calcula a soma dos divisores próprios de um número de forma otimizada.
    Divisores próprios são todos os divisores exceto o próprio número.
    
    Complexidade: O(√n)
    """
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
    """
    Verifica se um número é perfeito.
    Um número perfeito é igual à soma de seus divisores próprios.
    """
    return n > 0 and calcular_soma_divisores(n) == n

def encontrar_numeros_perfeitos(limite: int) -> List[int]:
    """
    Encontra todos os números perfeitos até o limite especificado.
    
    Utiliza a fórmula de Euclides para números perfeitos pares:
    Se 2^p - 1 é primo (primo de Mersenne), então 2^(p-1) * (2^p - 1) é perfeito.
    """
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
    """
    Verifica se dois números são amigáveis.
    Dois números são amigáveis se a soma dos divisores próprios de cada um
    é igual ao outro número.
    """
    return (a != b and 
            calcular_soma_divisores(a) == b and 
            calcular_soma_divisores(b) == a)

def encontrar_pares_amigaveis(limite: int) -> List[Tuple[int, int]]:
    """
    Encontra todos os pares de números amigáveis até o limite especificado.
    Otimizado para evitar cálculos duplicados.
    """
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

def analisar_intervalo(inicio: int, fim: int) -> Dict:
    """
    Analisa um intervalo e retorna informações sobre números perfeitos e amigáveis.
    """
    print(f"Analisando intervalo de {inicio} a {fim}...")
    
    # Encontrar números perfeitos no intervalo
    perfeitos = [n for n in encontrar_numeros_perfeitos(fim) if n >= inicio]
    
    # Encontrar pares amigáveis no intervalo
    todos_pares = encontrar_pares_amigaveis(fim)
    pares_no_intervalo = [
        par for par in todos_pares 
        if par[0] >= inicio or par[1] >= inicio
    ]
    
    return {
        'intervalo': (inicio, fim),
        'numeros_perfeitos': perfeitos,
        'pares_amigaveis': pares_no_intervalo,
        'total_perfeitos': len(perfeitos),
        'total_pares_amigaveis': len(pares_no_intervalo)
    }

def verificar_numero_especifico(n: int) -> Dict:
    """
    Analisa um número específico para verificar suas propriedades.
    """
    soma_divisores = calcular_soma_divisores(n)
    eh_perfeito = eh_numero_perfeito(n)
    
    # Verifica se tem par amigável
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

# Exemplo de uso e testes
if __name__ == "__main__":
    print("=== VERIFICADOR DE NÚMEROS PERFEITOS E AMIGÁVEIS ===\n")
    
    # Teste 1: Verificar números específicos
    print("1. Verificando números específicos:")
    numeros_teste = [6, 28, 220, 284, 496, 8128]
    
    for num in numeros_teste:
        resultado = verificar_numero_especifico(num)
        print(f"Número {num}:")
        print(f"  - Soma dos divisores próprios: {resultado['soma_divisores_proprios']}")
        print(f"  - É perfeito: {resultado['eh_perfeito']}")
        print(f"  - É amigável: {resultado['eh_amigavel']}")
        if resultado['par_amigavel']:
            print(f"  - Par amigável: {resultado['par_amigavel']}")
        print()
    
    # Teste 2: Encontrar números perfeitos até 10000
    print("2. Números perfeitos até 10.000:")
    perfeitos = encontrar_numeros_perfeitos(10000)
    print(f"Encontrados: {perfeitos}")
    print()
    
    # Teste 3: Encontrar pares amigáveis até 10000
    print("3. Pares amigáveis até 10.000:")
    pares = encontrar_pares_amigaveis(10000)
    print(f"Encontrados {len(pares)} pares:")
    for par in pares:
        print(f"  - {par[0]} e {par[1]}")
    print()
    
    # Teste 4: Análise de intervalo
    print("4. Análise do intervalo 1-5000:")
    resultado = analisar_intervalo(1, 5000)
    print(f"Números perfeitos: {resultado['numeros_perfeitos']}")
    print(f"Pares amigáveis: {resultado['pares_amigaveis']}")
    print(f"Total de perfeitos: {resultado['total_perfeitos']}")
    print(f"Total de pares amigáveis: {resultado['total_pares_amigaveis']}")