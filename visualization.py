import seaborn as sns
import matplotlib.pyplot as plt

def corr_matrix(matrix):
    sns.heatmap(matrix, annot=True, cmap='coolwarm', fmt=".2f")

    plt.title("Correlation Matrix Heatmap")
    plt.show()