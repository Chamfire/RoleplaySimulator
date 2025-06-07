import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.DataFrame({
    'id': ['A', 'B', 'C'],
    'Duración': [10, 15, 7],
    'Ha jugado antes': ['Sí', 'No', 'Sí']
})

sns.set_theme(style="whitegrid")
fig, ax = plt.subplots()

palette_custom = {'Sí': 'green', 'No': 'blue'}

sns.barplot(
    x='id',
    y='Duración',
    hue='Ha jugado antes',
    data=df,
    palette=palette_custom,
    ax=ax,
    errorbar=None
)

handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower right', fontsize='large', frameon=False)

plt.tight_layout()
plt.show()