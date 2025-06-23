import pandas as pd
import matplotlib.pyplot as plt

df1 = pd.read_csv('performance_report.csv')

plt.plot(df1['intervalo'], df1['tempo_execucao'], 
         marker='o', label='Método Sequencial', linewidth=2)


plt.xlabel('Intervalo', fontsize=12)
plt.ylabel('Tempo (s)', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig('Sequencial.png', dpi=300, bbox_inches='tight')

plt.show()