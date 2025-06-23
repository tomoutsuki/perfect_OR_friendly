import pandas as pd
import matplotlib.pyplot as plt

# Ler os arquivos CSV
df1 = pd.read_csv('sequencial.csv')
df2 = pd.read_csv('paralelo.csv')
df3 = pd.read_csv('distribuido.csv')

# Plotar as três retas
plt.plot(df1['intervalo'], df1['tempo_execucao'], 
         marker='o', label='Método Sequencial', linewidth=2)

plt.plot(df2['intervalo'], df2['tempo_execucao'], 
         marker='s', label='Método Paralelo', linewidth=2)

plt.plot(df3['intervalo'], df3['tempo_execucao'], 
         marker='^', label='Método Distribuído', linewidth=2)

plt.xlabel('Intervalo', fontsize=12)
plt.ylabel('Tempo (s)', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig('Comparação.png', dpi=300, bbox_inches='tight')

plt.show()