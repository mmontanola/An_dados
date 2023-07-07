from tratamento_dados import *
from funcoes_tratamento import *
from funcoes_graficos import *
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima.model import ARIMA
from pandas.tseries.offsets import DateOffset
import streamlit as st
import pandas as pd

@st.cache_data(ttl=3600)
def load_data():
    df_completo = pd.read_excel(fr'completa.xlsx',engine='openpyxl')
    # df_completo = Tratamento().tratamento_inicial_merge() # em PRD
    return df_completo

df_completo = load_data()

@st.cache_resource
def agrupamento_e_contar(coluna_agrupamento, operacao, coluna_conta, tabela_ou_grafico):
    ag = df_completo.groupby(coluna_agrupamento)
    ops = {
        'soma': ag[coluna_conta].sum(),
        'media': ag[coluna_conta].mean()
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
        st.plotly_chart(fig, use_container_width=True)


@st.cache_resource
def agrupamento_de_datas_e_categorias(coluna_agrupamento, operacao, coluna_conta, periodo, tabela_ou_grafico):
    # df_completo['shipping_limit_date'] = pd.to_datetime(df_completo['shipping_limit_date'])

    if periodo == 'mensal':
        df_completo['data_agrupada'] = df_completo['data limite de envio'].dt.to_period('M')
    elif periodo == 'semanal':
        df_completo['data_agrupada'] = df_completo['data limite de envio'].dt.to_period('W')
    elif periodo == 'diario':
        df_completo['data_agrupada'] = df_completo['data limite de envio'].dt.to_period('D')
    elif periodo == 'anual':
        df_completo['data_agrupada'] = df_completo['data limite de envio'].dt.to_period('Y')

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

        st.plotly_chart(fig, use_container_width=True)

    else:
        string_coluna = str(coluna_conta)
        tabelas_cidades_valor = tabelas_cidades_valor.sort_values(ascending=False, by=[string_coluna])
        tabelas_cidades_valor[string_coluna] = tabelas_cidades_valor[string_coluna].apply(lambda x: f'{x:,.2f}')
        st.table(tabelas_cidades_valor)


from statsmodels.tsa.arima.model import ARIMA
from pandas.tseries.offsets import DateOffset


def run_forecast(train):
    model = ARIMA(train, order=(5, 1, 0))
    model_fit = model.fit()

    future_dates = [train.index[-1] + DateOffset(days=x) for x in range(1, 91)]
    forecast_result = model_fit.forecast(steps=90)

    forecast_df = pd.DataFrame(forecast_result, index=future_dates, columns=['preço'])

    return forecast_df


def plot_data(df):
    fig = go.Figure(data=go.Scatter(x=df.index, y=df['preço'], mode='lines+markers'))
    fig.update_layout(title='Preço de Vendas ao Longo do Tempo',
                      xaxis_title='Data',
                      yaxis_title='Preço',
                      width=1200,
                      height=600)
    st.plotly_chart(fig, use_container_width=True)

def plot_forecast(train, forecast):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=train.index, y=train, mode='lines', name='Treino'))
    fig.add_trace(go.Scatter(x=forecast.index, y=forecast['preço'], mode='lines', name='Previsão'))
    fig.update_layout(showlegend=True)
    st.plotly_chart(fig)


def page_informacoes_gerais():
    st.title('Informações Gerais')
    # Total de vendas
    total_vendas = df_completo.shape[0]
    st.metric(label='Total de Vendas', value=total_vendas)

    # Tipo de pagamento mais utilizado
    tipo_pagamento_counts = df_completo['tipo de pagamento'].value_counts()
    st.bar_chart(tipo_pagamento_counts)

    # Parcelamentos mais utilizados
    parcelamentos_counts = df_completo['pagamento parcelado'].value_counts()
    st.bar_chart(parcelamentos_counts)

    # Nome da categoria mais utilizado
    categoria_counts = df_completo['nome da categoria do produto'].value_counts()
    st.bar_chart(categoria_counts)

    # Filtro por tipo de pagamento
    tipo_pagamento = st.selectbox('Filtrar por Tipo de Pagamento:', df_completo['tipo de pagamento'].unique())
    filtered_df = df_completo[df_completo['tipo de pagamento'] == tipo_pagamento]
    st.dataframe(filtered_df)

    # Filtro por nome de produto
    nome_produto = st.selectbox('Filtrar por Nome de Produto:', df_completo['nome da categoria do produto'].unique())
    filtered_df = df_completo[df_completo['nome da categoria do produto'] == nome_produto]
    st.dataframe(filtered_df)

def page_graficos_tabelas():
    st.title('Gráficos e Tabelas')
    # Configuração da barra lateral do Streamlit
    st.sidebar.title('Configurações')

    operacao = st.sidebar.selectbox('Selecione a operação:', ('soma', 'media', 'corr'))
    coluna_conta = st.sidebar.selectbox('Selecione a coluna para contar:',
                                        df_completo.select_dtypes(include=['number']).columns.tolist())
    coluna_agrupamento = st.sidebar.selectbox('Selecione a coluna para agrupar:', df_completo.columns)
    periodo = st.sidebar.selectbox('Selecione o período para agrupar:', ['anual', 'mensal', 'diario', 'semanal'])
    tabela_ou_grafico = st.sidebar.selectbox('Selecione a visualização:', ['tabela', 'grafico'])

    func_map = {
        'agrupamento_e_contar': agrupamento_e_contar,
        'agrupamento_de_datas_e_categorias': agrupamento_de_datas_e_categorias
    }

    func = st.sidebar.selectbox('Selecione a função:', list(func_map.keys()))
    func_map[func](coluna_agrupamento, operacao, coluna_conta, periodo, tabela_ou_grafico)



def page_previsao_precos():
    st.title('Previsão de Preços')
    df_preco = df_completo[['data limite de envio', 'preço']].copy()
    df_preco.set_index('data limite de envio', inplace=True)
    df_preco.sort_index(inplace=True)

    # Separamos os dados de treino e teste
    train = df_preco[:-90]
    test = df_preco[-90:]

    forecast = run_forecast(train)

    st.subheader('Previsão para os próximos 90 dias')
    st.dataframe(forecast)

    st.subheader('Gráfico de previsão')
    plot_forecast(train, forecast)

def page_anotacoes():
    st.title('Anotações')

    # Verifica se a chave 'notes' já existe no estado da sessão, caso contrário, inicializa com uma string vazia
    if 'notes' not in st.session_state:
        st.session_state['notes'] = ''

    # Mostra a área de texto widget, com o valor atual de st.session_state['notes']
    notes = st.text_area("Digite suas anotações aqui...", st.session_state['notes'])

    # Atualiza st.session_state['notes'] com qualquer novo texto que o usuário tenha inserido
    st.session_state['notes'] = notes

# Páginas ao Streamlit
pages = {
    'Informações Gerais': page_informacoes_gerais,
    'Gráficos e Tabelas': page_graficos_tabelas,
    'Previsão de Preços': page_previsao_precos,
    'Anotações': page_anotacoes
}

# Barra lateral para selecionar a página
page = st.sidebar.selectbox('Selecione a página:', list(pages.keys()))

# Executa a função correspondente à página selecionada
pages[page]()
