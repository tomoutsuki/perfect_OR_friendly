import socket
import pickle
import threading
import time
import csv
from datetime import datetime

# Definição de host do servidor como "localhost:12345".
HOST = 'localhost'
PORT = 12345

# Função para controlar a comunicação com o client-side.
def handle_client(conn, addr, intervalo):
    try:
        # Envio do intervalo via pickle.
        conn.sendall(pickle.dumps(intervalo))

        # Leitura dos dados da comunicação TCP (tamanho máximo de 4096bytes).
        data = conn.recv(4096)

        # Carrega os dados recebidos na array de resultados.
        result = pickle.loads(data)
        results.append(result)
    finally:
        # Fechar conexão mesmo em caso de erro.
        conn.close()

# Função que organiza a distribuição e agregação de resultados para um intervalo
def executar_distribuicao(inicio, fim, num_clients):
    global clients, results
    clients = []  # Resetar a lista de clientes
    results = []  # Resetar a lista de resultados

    # Criação de socket server-side
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Conexão do socket ao host e porta server-side.
        s.bind((HOST, PORT))
        s.listen() # Listen às conexões.

        print(f"\nAguardando conexão de {num_clients} clientes em {HOST}:{PORT}...")
        print(f"Distribuindo intervalo: {inicio} a {fim}")

        # Aguardar até todos os clientes conectarem ao servidor.
        while len(clients) < num_clients:
            # Aceitar conexão de cliente.
            conn, addr = s.accept()
            # conn: socket do cliente conectado.
            # addr: endereço do cliente conectado.
            clients.append((conn, addr))  # Adiciona dados do cliente conectado na array.
            print(f"Cliente conectado: {addr}")

        print("Iniciando distribuição de intervalos.")
        # Marcar início do tempo de execução
        tempo_inicio = time.time()
        # Contagem de números para cada intervalos em faixas
        step = (fim - inicio + 1) // num_clients
        # (ex: 1-10000 para 4 clientes, cada cliente fica com 2500 números para verificar)

        # Inicialização de threads.
        threads = []

        # Iteração para cada cliente conectado.
        for i, (conn, addr) in enumerate(clients):
            faixa_inicio = inicio + (i * step)

            if i == num_clients - 1:
                faixa_fim = fim
            else:
                faixa_fim = faixa_inicio + step - 1

            # Para cada função de controle de cliente, atribuir um thread.
            t = threading.Thread(target=handle_client, args=(conn, addr, (faixa_inicio, faixa_fim)))
            t.start() # Inicia a thread
            threads.append(t) # Adição da thread na lista de threads.

        # Aguarda todos os clientes (todas as threads) terminarem o processo
        for t in threads:
            t.join()

        # Marcar fim do tempo de execução
        tempo_fim = time.time()
        tempo_execucao = tempo_fim - tempo_inicio

        # Array para armazenar resultados.
        numeros_perfeitos = []
        pares_amigaveis = []

        # Adicionar resultados no array de números perfeitos/amigáveis.
        for res in results:
            numeros_perfeitos.extend(res['numeros_perfeitos'])
            pares_amigaveis.extend(res['pares_amigaveis'])

        print("\n=== RESULTADOS AGREGADOS ===")
        print(f"Tempo de execução: {tempo_execucao:.4f} segundos")
        print("Números perfeitos encontrados:", sorted(set(numeros_perfeitos)))
        print("Pares amigáveis encontrados:", sorted(set(map(tuple, map(sorted, pares_amigaveis)))))

        return {
            'intervalo': f"{inicio}-{fim}",
            'quantidade_clientes': num_clients,
            'tempo_execucao': tempo_execucao
        }

def salvar_csv(resultados, nome_arquivo=None):
    """Salva os resultados em um arquivo CSV"""
    if nome_arquivo is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"resultados_performance_{timestamp}.csv"
    
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['intervalo', 'quantidade_clientes', 'tempo_execucao']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for resultado in resultados:
            writer.writerow(resultado)

def main():
    num_clients = int(input("Número de clientes esperados: "))
    
    # Lista para armazenar todos os resultados
    todos_resultados = []

    # Executar a função com 3 intervalos diferentes
    resultado1 = executar_distribuicao(1, 100000, num_clients)
    todos_resultados.append(resultado1)
    
    resultado2 = executar_distribuicao(1, 500000, num_clients)
    todos_resultados.append(resultado2)
    
    resultado3 = executar_distribuicao(1, 1000000, num_clients)
    todos_resultados.append(resultado3)
    
    # Salvar resultados em CSV
    salvar_csv(todos_resultados)

if __name__ == "__main__":
    main()