import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('medical_examination.csv') # lê o arquivo e guarda em df

# Criar a coluna 'overweight' com base no IMC
bmi = df['weight'] / ((df['height'] / 100) ** 2) # calcula o IMC de cada pessoa
df['overweight'] = (bmi > 25).astype(int) # adiciona coluna: 1 = acima do peso, 0 = não

# Normaliza colesterol e glicose
# Se valor for 1, significa normal --> 0 (bom)
# Se valor for 2 ou 3, significa ruim --> 1 (ruim)
df['cholesterol'] = (df['cholesterol'] > 1).astype(int) # normaliza colesterol
df['gluc'] = (df['gluc'] > 1).astype(int) # normaliza glicose


# Transformar os dados em formato "longo" com melt
def draw_cat_plot():
    df_cat = pd.melt(
        df,
        id_vars = ['cardio'], # mantém a coluna cardio fixa
        value_vars = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'] # colunas para serem comparadas
    )

    # Agrupar por cardio, variável e valor, depois contar quantas vezes aparece
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name = 'total')


    # gráfico de barras com seaborn (catplot)

    g = sns.catplot(
        data = df_cat,
        x = 'variable', # eixo x será a variável (coluna analisada) 
        y = 'total', # eixo y será o total de contagens
        hue = 'value', # divide as barras pela coluna value (0 ou 1)
        col = 'cardio', # cria um gráfico para cardio=0 e outro para cardio=1
        kind = 'bar' # tipo de gráfico: barras
    )
    

    # Salvar gráfico como imagem e retornar

    fig = g.fig
    fig.savefig('catplot.png')
    return fig

# 10
def draw_heat_map():
    # Limpar os dados --> incorretos ou otliers
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) & # pressão diastólica não pode ser maior que a sistólica
        (df['height'].between(df['height'].quantile(0.025), df['height'].quantile(0.975))) & # altura dentro de 95% do intervalo
        (df['weight'].between(df['weight'].quantile(0.025), df['weight'].quantile(0.975))) # peso dentro de 95% do intervalo
    ]

    # Calcula a matriz de correlação entre as variáveis numéricas
    corr = df_heat.corr(numeric_only = True)

    # Cria máscara para esconder metade superior da matriz pra evitar repetição
    mask = np.triu(np.ones_like(corr, dtype = bool))



    # Cria figura do matplotlib com tamanho definido
    fig, ax = plt.subplots(figsize = (10, 8))
    sns.heatmap(
        corr, # matriz de correlação
        mask = mask, # aplica máscara
        annot = True, # mostra valores dentro do heatmap
        fmt = '.1f', # formata valores com 1 casa decimal
        square = True, # quadrados perfeitos
        cbar_kws = {"shrink": .5} # barra de cores menor
    )

    # Salva o heatmap como imagem e retorna
    fig.savefig('heatmap.png')
    return fig

    # Executa as funções quando o arquivo for rodado diretamente
    if __name__ == '__main__':
        draw_cat_plot() # gera o gráfico categórico
        draw_heat_map() # gera o heatmap


