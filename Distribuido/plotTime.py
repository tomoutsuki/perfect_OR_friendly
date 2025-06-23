import pandas as pd
import matplotlib.pyplot as plt

# Ler o arquivo CSV
df = pd.read_csv('resultados_performance.csv')

plt.plot(df['intervalo'], df['tempo_execucao'], 
         marker='o', label='Método Distribuído', linewidth=2)

plt.xlabel('Intervalo', fontsize=12)
plt.ylabel('Tempo (s)', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig('Distribuído.png', dpi=300, bbox_inches='tight')

plt.show()