import pandas as pd
import os
from deep_translator import GoogleTranslator
import seaborn as sns
import matplotlib.pyplot as plt
from ydata_profiling import ProfileReport
import sweetviz as sv
import pandas as pd
import plotly.express as px
import pandas as pd
import os
from deep_translator import GoogleTranslator
import seaborn as sns
import matplotlib.pyplot as plt
from ydata_profiling import ProfileReport
import sweetviz as sv
import pandas as pd
import plotly.express as px
import pandas as pd
import os
from deep_translator import GoogleTranslator
import seaborn as sns
import matplotlib.pyplot as plt
from ydata_profiling import ProfileReport
import sweetviz as sv
# import dtale
from funcoes_graficos import *
import pandas as pd
import numpy as np
import pmdarima as pm
from matplotlib import pyplot as plt


class Tratamento:

    def __init__(self):
        self.local = fr'C:\Users\matheus.montanola\PycharmProjects\Oficial_An_dados\planilhas'
        self.pasta = os.listdir(r'C:\Users\matheus.montanola\PycharmProjects\Oficial_An_dados\planilhas')
        self.definir_planilhas_de_trabalho()

    def box_plot_temp_rapido(self):
        for i in self.pasta:
            df = pd.read_csv(fr'{self.local}/{i}')
            translated_df = Funcoes_tratamentos.translate_and_replace_columns(df)
            Funcoes_tratamentos.plot_correlation_heatmap(translated_df, i)

    def verificar_header_planilhas(self):
        for i in self.pasta:
            df = pd.read_csv(fr'{self.local}/{i}')
            print(i)
            print(df.head(3))
            print('----------------------------------------------')

############### Descrição planilha ########################
# ok olist_order_items_dataset.csv ==== Localização do cliente - usar customer_unique_id ou Identificação do Cliente - 'cidade_cliente', 'cliente_estado'
# ok Mais importante -- olist_order_items_dataset.csv ==== 'pedido_id', 'pedido_item_id', 'ID do produto', 'vendedor_id'
# ok - olist_order_payments_dataset.csv ===== 'pedido_id' -- mostrar 'tipo de pagamento', 'pagamento_parcelas', 'valor_pagamento']
# ok - olist_products_dataset.csv ====== 'ID do produto' --- mostrar 'product_category_name'
# olist_sellers_dataset.csv ==== 'vendedor_id' - mostrar 'vendedor_cidade', 'vendedor_estado'

    def definir_planilhas_de_trabalho(self):
        self.df_master_pedidos = pd.read_csv(fr'C:\Users\matheus.montanola\PycharmProjects\Oficial_An_dados\planilhas\olist_order_items_dataset.csv')
        self.df_cliente_localizacao = pd.read_csv(fr'C:\Users\matheus.montanola\PycharmProjects\Oficial_An_dados\planilhas\olist_customers_dataset.csv')
        self.df_modo_de_pagamento = pd.read_csv(fr'C:\Users\matheus.montanola\PycharmProjects\Oficial_An_dados\planilhas\olist_order_payments_dataset.csv')
        self.df_vendedor_localizacao= pd.read_csv(fr'C:\Users\matheus.montanola\PycharmProjects\Oficial_An_dados\planilhas\olist_sellers_dataset.csv')
        self.df_categoria_produto = pd.read_csv(fr'C:\Users\matheus.montanola\PycharmProjects\Oficial_An_dados\planilhas\olist_products_dataset.csv')

    def tratamento_inicial_merge(self):

        # Merge de master_pedidos com modo_de_pagamento
        self.df_completo = pd.merge(self.df_master_pedidos, self.df_modo_de_pagamento, on='order_id', how='left')
        # print(self.df_completo['order_id'].count())
        # print(self.df_master_pedidos['order_id'].count())

        # Merge do DataFrame completo com categoria_produto
        df_completo = pd.merge(self.df_completo, self.df_categoria_produto, on='product_id',how='left')

        # Merge do DataFrame completo com vendedor_localizacao
        df_completo = pd.merge(df_completo, self.df_vendedor_localizacao, on='seller_id', suffixes=('', '_seller'),how='left')
        df_completo = df_completo[['order_id','product_id','seller_id','shipping_limit_date','price','freight_value','payment_type','payment_installments','product_category_name','seller_city','seller_state']]

        # df_completo = df_completo[['order_id','product_id','seller_id','shipping_limit_date',	'price','freight_value','payment_type','payment_installments','product_category_name','product_name_lenght','product_description_lenght','product_photos_qty','product_weight_g','product_length_cm','product_height_cm','product_width_cm','seller_zip_code_prefix','seller_city','seller_state']]
        df_completo.drop_duplicates(ignore_index=True,inplace=True)
        # print(df_completo.columns)

        df_completo['payment_type'] = df_completo['payment_type'].astype('category')
        df_completo['payment_installments'] = df_completo['payment_installments'].astype('category')
        df_completo['product_category_name'] = df_completo['product_category_name'].astype('category')
        df_completo['seller_city'] = df_completo['seller_city'].astype('category')
        df_completo['seller_state'] = df_completo['seller_state'].astype('category')
        df_completo['order_id'] = df_completo['order_id'].astype('category')
        df_completo['product_id'] = df_completo['product_id'].astype('category')
        df_completo['seller_id'] = df_completo['seller_id'].astype('category')
        df_completo['shipping_limit_date'] = pd.to_datetime(df_completo['shipping_limit_date'])

        df_completo = Funcoes_tratamentos().translate_and_replace_columns(df_completo)


        df_completo.to_excel('completa.xlsx',index=False)
        return df_completo

    def relatorios_html(self):
        df = self.tratamento_inicial_merge()
        profile = ProfileReport(df, title="Relatório de Análise Exploratória -  ProfileReport", explorative=True)
        #Salve o relatório como um arquivo HTML
        profile.to_file("Relatorio_ProfileReport.html")

        report = sv.analyze(df)
        #Salve o relatório como um arquivo HTML
        report.show_html("Relatorio_Sweetviz.html")

        return print(os.getcwd())


if __name__ == "__main__":
    Tratamento().tratamento_inicial_merge()