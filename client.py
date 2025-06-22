import socket
import pickle
from perfect_or_friendly_seq import analisar_intervalo # Carregar lógica de solução da abordagem sequencial

# Definição de host do servidor como "localhost:12345"
HOST = 'localhost'
PORT = 12345

def main():
    # Criação de socket client-side
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # Leitura dos intervalos distribuídos pelo servidor.
        s.connect((HOST, PORT)) # Conexão ao servidor
        data = s.recv(1024) # Leitura dos dados da comunicação TCP (tamanho máximo de 1024bytes)
        intervalo = pickle.loads(data) # Recebe a array dos intervalos (ex: [1, 10000])

        print(f"Intervalo recebido: {intervalo}")

        # Chamada da função "analisar_intervalo()" da abordagem sequencial.
        resultado = analisar_intervalo(intervalo[0], intervalo[1])
        
        # Envia os resultados para o servidor via pickle.
        s.sendall(pickle.dumps(resultado))

if __name__ == "__main__":
    main()
