# visualize.py
import matplotlib.pyplot as plt
import seaborn as sns

def plot_style_trend(style_time):
    plt.figure(figsize=(6,4))
    sns.lineplot(data=style_time, x='week', y='count', hue='style', marker='o')
    plt.title("Weekly New Products by Style")
    plt.xlabel("Week")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_color_distribution(df):
    plt.figure(figsize=(4,3))
    color_counts = df['color'].value_counts()
    sns.barplot(x=color_counts.values, y=color_counts.index, palette='pastel')
    plt.title("Product Count by Color")
    plt.xlabel("Count")
    plt.ylabel("Color")
    plt.tight_layout()
    plt.show()
