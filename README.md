# Projeto de Análise de Dados

Este projeto é uma aplicação de análise de dados construída em Python, utilizando bibliotecas como Pandas, Streamlit, Plotly, entre outras. O objetivo é fornecer uma interface interativa para explorar, visualizar e analisar dados.

## Estrutura do Projeto

O projeto é composto por três arquivos principais:

1. `tratamento_dados.py`
2. `funcoes_tratamento.py`
3. `main.py`

### `tratamento_dados.py`

Este arquivo contém a classe `Tratamento`, que é responsável por carregar e processar os dados. Ela realiza várias operações, como leitura de arquivos, limpeza e transformação de dados, e geração de relatórios de análise exploratória.

### `funcoes_tratamento.py`

Este arquivo contém a classe `Funcoes_tratamentos`, que fornece várias funções úteis para o tratamento de dados, como tradução de texto, renomeação de colunas de DataFrame, e geração de gráficos de correlação.

### `main.py`

Este é o script principal que utiliza as funções definidas nos outros dois arquivos para realizar a análise de dados. Ele também usa a biblioteca Streamlit para criar uma aplicação web interativa para visualizar os resultados. A aplicação inclui várias páginas, como 'Informações Gerais', 'Gráficos e Tabelas', 'Previsão de Preços', e 'Anotações'.

## Como Usar

Para usar esta aplicação, você precisará ter Python instalado em seu sistema, juntamente com as bibliotecas necessárias. Você pode instalar as bibliotecas usando o seguinte comando:

```bash
pip install -r requirements.txt
```

Depois de instalar as dependências, você pode iniciar a aplicação com o seguinte comando:

```bash
streamlit run main.py
```

Isso iniciará a aplicação Streamlit em seu navegador. Você pode então interagir com a aplicação para explorar e analisar os dados.

## Contribuindo

Contribuições para este projeto são bem-vindas. Se você encontrar um bug ou tiver uma sugestão para uma nova funcionalidade, por favor, abra uma issue. Se você quiser contribuir com código, por favor, abra um pull request.

## Licença

Este projeto é licenciado sob os termos da Licença MIT. Veja o arquivo LICENSE para mais detalhes.
