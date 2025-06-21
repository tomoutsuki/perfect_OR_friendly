# perfect_OR_friendly
Projeto desenvolvido para atividade final na disciplina de *Sistemas Distribuídos (EC48A)*.

### ・Objetivo:
Resolução do problema de **verificação de números perfeitos ou números amigáveis** em grandes intervalos, computacionalmente paralelizável. 
O projeto é implementado de três abordagens diferentes:

- **Versão Sequencial**
- **Versão Paralela com Threads**
- **Versão Distribuída com Sockets TCP**

Ao final, os tempos de execução de cada abordagem são comparados em diferentes escalas de entrada, permitindo analisar **eficiência, escalabilidade** e identificar **gargalos** computacionais.

---

### ・Conceitos Envolvidos

- **Número Perfeito**: número igual à soma de seus divisores próprios (ex: 6 → 1 + 2 + 3 = 6)
- **Números Amigáveis**: pares de números cujas somas dos divisores próprios de um é igual ao outro (ex: 220 e 284)
- **Threading em Python** (`threading.Thread`)
- **Programação Distribuída** via sockets TCP (`socket`)
- **Análise de desempenho** e coleta de tempo de execução

---

### ・Integrantes

Projeto realizado por um grupo de 4 integrantes:
- Emily Miho Yoshizawa
- Guilherme Mauricio Aguero Giaciani
- Mateus Amorim de Oliveira
- Tom Outsuki

---

### ・Metodologia de Testes

- Intervalos de teste `1 a X`, `1 a Y`, `1 a Z` (ex: 1-1000, 1-10.000, 1-100.000)
- Cada execução é repetida X vezes e a média dos tempos é calculada para comparação.
- 
- Métricas observadas:
- Ferramentas de medição: `time`, `perf_counter` (Python)

---

### ・Etapas para Execução

1. a
2. a
3. a
