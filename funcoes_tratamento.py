from tratamento_dados import *
import pandas as pd

class Configuracoes:
    def __init__(self):
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_rows', 15)


class Funcoes_tratamentos:
    def __init__(self):
        Configuracoes()
        return

    def translate_text(self, text):
        # Substituir os underscores por espaços
        text = text.replace("_", " ")
        # Traduzir o texto
        translated_text = GoogleTranslator(source='en', target='pt').translate(text)
        return translated_text

    def translate_and_replace_columns(self, df):
        # Traduzir cada coluna e criar um dicionário de mapeamento
        translated_columns = [self.translate_text(column) for column in df.columns]
        translated_columns_dict = dict(zip(df.columns, translated_columns))
        # Renomear as colunas do DataFrame
        df.rename(columns=translated_columns_dict, inplace=True)
        return df

    def plot_correlation_heatmap(self,df, title):
        # Selecionar apenas colunas numéricas
        numeric_columns = df.select_dtypes(include=['number'])

        # Calcular a matriz de correlação
        corr_matrix = numeric_columns.corr()

        # Criar um heatmap de correlação usando a biblioteca Seaborn
        plt.figure(figsize=(12, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title(title)
        plt.show()