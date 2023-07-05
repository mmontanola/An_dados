from tratamento_dados import *
from funcoes_tratamento import *
from funcoes_graficos import *


def agrupamento_e_contar(coluna_agrupamento, operacao, coluna_conta, tabela_ou_grafico):
    ag = df_completo.groupby(coluna_agrupamento)
    ops = {
        'soma': ag[coluna_conta].sum(),
        'media': ag[coluna_conta].mean(),
        'corr': ag.apply(lambda x: x[coluna_conta].corr(x['freight_value']))  # calcula a correlação dentro de cada grupo
    }
    tabelas_cidades_valor = ops[operacao]
    tabelas_cidades_valor = tabelas_cidades_valor.sort_values(ascending=False)
    tabelas_cidades_valor_formatado = tabelas_cidades_valor.apply(lambda x: f'{x:,.2f}')

    if tabela_ou_grafico == 'tabela':
        st.table(tabelas_cidades_valor_formatado)
    else:
        # Combine todas as linhas além das 15 primeiras em 'Outros'
        outros = tabelas_cidades_valor.iloc[15:].sum()
        tabelas_cidades_valor = tabelas_cidades_valor.iloc[:15]
        outros_series = pd.Series([outros], index=['Outros'])
        tabelas_cidades_valor = pd.concat([tabelas_cidades_valor, outros_series])

        # Transformar a série em DataFrame para o Plotly Express
        tabelas_cidades_valor_df = tabelas_cidades_valor.reset_index()
        tabelas_cidades_valor_df.columns = [coluna_agrupamento, coluna_conta]

        fig = px.pie(tabelas_cidades_valor_df, values=coluna_conta, names=coluna_agrupamento, title=coluna_agrupamento,
                     hover_data=[coluna_conta], labels={coluna_conta: 'Informações'},
                     hole=.3,width=2500,height=900)

def agrupamento_de_datas_e_categorias(coluna_agrupamento, operacao, coluna_conta, periodo, tabela_ou_grafico):
    df_completo['shipping_limit_date'] = pd.to_datetime(df_completo['shipping_limit_date'])

    if periodo == 'mensal':
        df_completo['data_agrupada'] = df_completo['shipping_limit_date'].dt.to_period('M')
    elif periodo == 'semanal':
        df_completo['data_agrupada'] = df_completo['shipping_limit_date'].dt.to_period('W')
    elif periodo == 'diario':
        df_completo['data_agrupada'] = df_completo['shipping_limit_date'].dt.to_period('D')
    elif periodo == 'anual':
        df_completo['data_agrupada'] = df_completo['shipping_limit_date'].dt.to_period('Y')

    ag = df_completo.groupby([coluna_agrupamento, 'data_agrupada'], as_index=False)
    ops = {
        'soma': ag[coluna_conta].sum(),
        'media': ag[coluna_conta].mean()
    }
    tabelas_cidades_valor = ops[operacao]
    tabelas_cidades_valor['data_agrupada'] = tabelas_cidades_valor['data_agrupada'].dt.to_timestamp()

    if tabela_ou_grafico == 'grafico':
        fig = px.bar(tabelas_cidades_valor,
                     x='data_agrupada',
                     y=coluna_conta,
                     color=coluna_agrupamento,
                     title=coluna_agrupamento,
                     labels={coluna_conta: 'Valor da Conta', 'data_agrupada': 'Data'},
                     hover_data=[coluna_conta])  # Exibindo dados adicionais ao passar o mouse sobre as barras

        fig.update_layout(barmode='group',
                          xaxis_title='Data',
                          yaxis_title='Valor da Conta',
                          legend_title_text=coluna_agrupamento,
                          height=900,
                          width=2500)

    else:
        string_coluna = str(coluna_conta)
        tabelas_cidades_valor = tabelas_cidades_valor.sort_values(ascending=False, by=[string_coluna])
        tabelas_cidades_valor[string_coluna] = tabelas_cidades_valor[string_coluna].apply(lambda x: f'{x:,.2f}')
