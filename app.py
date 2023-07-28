#para rodar o aplicativo a aplicação: python -m streamlit run app.py

#libs
import pandas as pd

#libs gráficas
import plotly.express as px
from plotly.subplots import make_subplots

#streamlit
import streamlit as st

#funções
def formata_numero_cartao(valor, prefixo = '', sufixo = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões {sufixo}'

#layout

st.set_page_config(layout = 'wide')

#lendo a base de dados

dados = pd.read_csv('dados_uteis.csv')

#tabelas

#tab1
evolucao_valores_exportacao = dados.groupby('ano').sum().drop('pais', axis = 1)

acumulado_top_10_mercados = pd.DataFrame(dados.groupby('pais').sum()[['quantidade_exportacao', 'valor_exportacao']])
selecao = acumulado_top_10_mercados.sort_values('valor_exportacao', ascending = False).head(10).index #selecionando os 10 maiores mercados de exportação
acumulado_top_10_mercados = acumulado_top_10_mercados.loc[selecao]
acumulado_top_10_mercados.reset_index(inplace = True)

selecao = acumulado_top_10_mercados['pais'].to_list()
evolucao_top_10 = dados[dados.pais.isin(selecao)]

#tab2
evolucao_quantidade_exportacao = dados.groupby('ano').sum().drop('pais', axis = 1)

#tab3
evolucao_preco_medio_por_litro = dados.groupby('ano').mean('valor_exportacao_por_litro').round(2)

preco_medio_por_litro_top_10 = evolucao_top_10[['pais', 'valor_exportacao_por_litro']].groupby('pais').mean().round(2)

percentual_exportacao = dados[['ano', 'pais', 'percentual_exportacao']].round(2)
evolucao_percentual_medio_exportacao = percentual_exportacao.groupby('ano').mean('percentual_exportacao').round(2)

percentual_medio_exportacao_top_10 = evolucao_top_10.groupby('pais').mean('percentual_exportacao').round(2)

index = evolucao_top_10.query('quantidade_exportacao == 0').index.to_list()
distribuicao_quantidade_valor_top_10 = evolucao_top_10.drop(index)
distribuicao_quantidade_valor_top_10.head()

#gráficos

#tab1
fig_evolucao_valores_exportacao = px.line(
    evolucao_valores_exportacao, 
    x = evolucao_valores_exportacao.index, 
    y = 'valor_exportacao',
    color_discrete_sequence = ['#673E69'])
fig_evolucao_valores_exportacao.update_layout(
    title = '', 
    xaxis_title = 'Período', 
    yaxis_title = 'Valor (US$)', 
    showlegend = False, 
    height = 600)

fig_acumulado_top_10_mercados_bar = px.bar(
    data_frame = acumulado_top_10_mercados,
    x = 'pais',
    y = 'valor_exportacao',
    color_discrete_sequence = ['#673E69'])
fig_acumulado_top_10_mercados_bar.update_layout(
    title = 'Bar', 
    xaxis_title = 'Países', 
    yaxis_title = 'Valor (US$)', 
    showlegend = False, 
    height = 600, 
    bargap = 0.1)

fig_acumulado_top_10_mercados_treemap = px.treemap(acumulado_top_10_mercados, path = ['pais'], values = 'valor_exportacao', title = 'Treemap', height = 600)
fig_acumulado_top_10_mercados_treemap.update_traces(root_color = '#673E69')

fig_evolucao_valores_top_10_line = px.line(
    data_frame = evolucao_top_10, 
    x = 'ano', 
    y = 'valor_exportacao',
    color = 'pais')
fig_evolucao_valores_top_10_line.update_layout(
    title = 'Time series', 
    xaxis_title = 'Período', 
    yaxis_title = 'Valor (US$)', 
    legend_title = 'Legenda',
    height = 600)

fig_evolucao_valores_top_10_treemap = px.treemap(evolucao_top_10, path = ['ano', 'pais'], values = 'valor_exportacao', title = 'Treemap', height = 600)
fig_evolucao_valores_top_10_treemap.update_traces(root_color = '#673E69')

#tab2
fig_evolucao_quantidade_exportacao = px.line(
    evolucao_quantidade_exportacao, 
    x = evolucao_quantidade_exportacao.index, 
    y = 'quantidade_exportacao',
    color_discrete_sequence = ['#D8D87C'])
fig_evolucao_quantidade_exportacao.update_layout(
    title = '', 
    xaxis_title = 'Países', 
    yaxis_title = 'Quantidade (Litros)', 
    showlegend = False, 
    height = 600)

fig_acumulado_top_10_mercados_line = px.bar(
    data_frame = acumulado_top_10_mercados,
    x = 'pais',
    y = 'quantidade_exportacao',
    color_discrete_sequence = ['#D8D87C']
    )
fig_acumulado_top_10_mercados_line.update_layout(
    title = 'Bar', 
    xaxis_title = 'Países', 
    yaxis_title = 'Valor (US$)', 
    showlegend = False, 
    height = 600, 
    bargap = 0.1
    )

fig_acumulado_top_10_mercados_treemap = px.treemap(acumulado_top_10_mercados, path = ['pais'], values = 'quantidade_exportacao', title = 'Treemap', height = 600)
fig_acumulado_top_10_mercados_treemap.update_traces(root_color = '#D8D87C')

fig_evolucao_quantidade_top_10_line = px.line(
data_frame = evolucao_top_10, 
x = 'ano', 
y = 'quantidade_exportacao',
color = 'pais')
fig_evolucao_quantidade_top_10_line.update_layout(
    title = 'Time series', 
    xaxis_title = 'Período', 
    yaxis_title = 'Quantidade (Litros)', 
    legend_title = 'Legenda',
    height = 600)

fig_evolucao_quantidade_top_10_treemap = px.treemap(evolucao_top_10, path = ['ano', 'pais'], values = 'quantidade_exportacao', title = 'Treemap', height = 600)
fig_evolucao_quantidade_top_10_treemap.update_traces(root_color = '#D8D87C')

#tab3
fig_evolucao_preco_medio_por_litro = px.line(
        data_frame = evolucao_preco_medio_por_litro, 
        x = evolucao_preco_medio_por_litro.index, 
        y = 'valor_exportacao_por_litro',
        color_discrete_sequence = ['#673E69'])
fig_evolucao_preco_medio_por_litro.update_layout(
    title = 'Time series', 
    xaxis_title = 'Período', 
    yaxis_title = 'Valor (US$$)',
    height = 600)

fig_preco_medio_por_litro_top_10_bar = px.bar(
    data_frame = preco_medio_por_litro_top_10, 
    x = preco_medio_por_litro_top_10.index, 
    y = 'valor_exportacao_por_litro',
    color_discrete_sequence = ['#673E69'])
fig_preco_medio_por_litro_top_10_bar.update_layout(
    title = 'Bar', 
    xaxis_title = 'Países', 
    yaxis_title = 'Valor (US$)', 
    height = 600,
    bargap = 0.1)

fig_preco_medio_por_litro_top_10_treemap = px.treemap(preco_medio_por_litro_top_10, path = [preco_medio_por_litro_top_10.index], values = 'valor_exportacao_por_litro', title = 'Treemap', height = 600)
fig_preco_medio_por_litro_top_10_treemap.update_traces(root_color = '#673E69')

fig_evolucao_valor_por_litro_top_10 = px.line(
    data_frame = evolucao_top_10, 
    x = 'ano', 
    y = 'valor_exportacao_por_litro',
    color = 'pais')
fig_evolucao_valor_por_litro_top_10.update_layout(
    title = 'Time series', 
    xaxis_title = 'Período', 
    yaxis_title = 'Valor (US$)', 
    legend_title = 'Legenda',
    height = 600)

fig_evolucao_percentual_medio_exportacao = px.line(
    data_frame = evolucao_percentual_medio_exportacao, 
    x = evolucao_percentual_medio_exportacao.index, 
    y = 'percentual_exportacao',
    color_discrete_sequence = ['#673E69'])
fig_evolucao_percentual_medio_exportacao.update_layout(
    title = 'Time series', 
    xaxis_title = 'Período', 
    yaxis_title = '%',
    height = 600)

fig_percentual_medio_exportacao_top_10_bar = px.pie(percentual_medio_exportacao_top_10, values = 'percentual_exportacao', names = percentual_medio_exportacao_top_10.index, title = 'Pie')

fig_percentual_medio_exportacao_top_10_treemap = px.treemap(percentual_medio_exportacao_top_10, path = [percentual_medio_exportacao_top_10.index], values = 'percentual_exportacao', title = 'Treemap', height = 600)
fig_percentual_medio_exportacao_top_10_treemap.update_traces(root_color = '#673E69')

fig_evolucao_percentual_medio_exportacao_top_10 = px.line(
    data_frame = evolucao_top_10, 
    x = 'ano', 
    y = 'percentual_exportacao',
    color = 'pais')
fig_evolucao_percentual_medio_exportacao_top_10.update_layout(
    title = 'Time series', 
    xaxis_title = 'Período', 
    yaxis_title = '%', 
    legend_title = 'Legenda',
    height = 600)

fig_distribuicao_valor_top_10 = px.scatter(
    data_frame = distribuicao_quantidade_valor_top_10, 
    x = 'pais', 
    y = 'ano', 
    size = 'valor_exportacao', 
    color = px.Constant('Valor (US$)'),
    color_discrete_sequence = ['#673E69'])
fig_distribuicao_valor_top_10.update_layout(
    title = 'Bubble', 
    xaxis_title = 'Países', 
    yaxis_title = 'Ano', 
    legend_title = 'Legenda',
    height = 700)
fig_distribuicao_valor_top_10.update_traces(marker = dict(size = 3.5 * distribuicao_quantidade_valor_top_10['valor_exportacao']))

fig_distribuicao_quantidade_top_10 = px.scatter(
    data_frame = distribuicao_quantidade_valor_top_10, 
    x = 'pais', 
    y = 'ano', 
    size = 'quantidade_exportacao', 
    color = px.Constant('Quantidade (Litros)'),
    color_discrete_sequence = ['#D8D87C'])
fig_distribuicao_quantidade_top_10.update_layout(
    title = 'Bubble', 
    xaxis_title = 'Países', 
    yaxis_title = 'Ano', 
    legend_title = 'Legenda',
    height = 700)
fig_distribuicao_valor_top_10.update_traces(marker = dict(size = 3.5 * distribuicao_quantidade_valor_top_10['quantidade_exportacao']))

#visualização no streamlit

#título da aplicação
st.title('Evolução da Exportação de Vinho Brasileiro nos Últimos 15 Anos')

#layout do aplicativo
tab0, tab1, tab2, tab3 = st.tabs(['Geral', 'Valor', 'Quantidade', 'Estatísticas'])

#separando as tabs
with tab0:

    #texto
    '''
    ## Dados e estatísticas da exportação de vinhos da Vitibrasil nos últimos 15 anos

    Base de dados Vitibrasil

    http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06

    A Vitibrasil uma organização associada à Embrapa, que tem como objetivo fornecer informações sobre a produção de uvas no estado do Rio Grande do Sul, que podem ser encontradas em seu website.
    Este dashboard apresenta os principais dados e estatísticas a respeito da exportação de vinho brasileiro nos últimos 15 anos.
    '''
    #dataFrame
    df = pd.DataFrame(dados)

    #tratando dados para visualização
    df['ano'] = df['ano'].astype(str).to_list()
    df.columns = ['Ano', 'País', 'Quantidade Importada (L)', 'Valor de Importação (US$)', 'Valor por Litro Importado (US$)', 
    'Quantidade Exportada (L)', 'Valor de Exportação (US$)', 'Valor por Litro Exportado (US$)', 'Produção Brasileira Total (L)', 
    'Percentual da Produção Exportado (%)']

    st.dataframe(df, use_container_width = True)

with tab1:

    #cartões
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('**Valor Total**', formata_numero_cartao(dados['valor_exportacao'].sum(), 'US$'))
    with coluna2:
        st.metric('**Valor Total em 2021**', formata_numero_cartao(dados.query('ano == 2021')['valor_exportacao'].sum(), ''))
    
    #evolução dos valores exportados
    st.markdown('**Evolução dos Valores Negociados**')
    st.plotly_chart(fig_evolucao_valores_exportacao, use_container_width = True)

    #acumulado valor
    st.markdown('**Acumulado dos Valores para os Principais Importadores**')
    coluna3, coluna4 = st.columns(2)
    with coluna3:
        #bar
        st.plotly_chart(fig_acumulado_top_10_mercados_bar, use_container_width = True)
    with coluna4:
        #treemap
        st.plotly_chart(fig_acumulado_top_10_mercados_treemap, use_container_width = True)

    #evolução de valores exportados top 10
    st.markdown('**Evolução dos Valores para os Principais Importadores**')
    #line
    st.plotly_chart(fig_evolucao_valores_top_10_line, use_container_width = True)
    #treemap
    st.plotly_chart(fig_evolucao_valores_top_10_treemap, use_container_width = True)

with tab2:

    #cartões
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('**Quantidade Total**', formata_numero_cartao(dados['quantidade_exportacao'].sum(), '', 'de litros'))
    with coluna2:
        st.metric('**Quantidade Total em 2021**', formata_numero_cartao(dados.query('ano == 2021')['quantidade_exportacao'].sum(), '', 'de litros'))
    
    #evolução da quantidade exportada
    st.markdown('**Evolução da Quantidade Negociada**')
    st.plotly_chart(fig_evolucao_quantidade_exportacao, use_container_width = True)

    #acumulado quantidade
    st.markdown('**Acumulado da Exportação para os Principais Importadores**')
    coluna3, coluna4 = st.columns(2)
    with coluna3:
        #bar 
        st.plotly_chart(fig_acumulado_top_10_mercados_line, use_container_width = True)
    with coluna4:
        #treemap
        st.plotly_chart(fig_acumulado_top_10_mercados_treemap, use_container_width = True)

    #evolução da quantidade exportada top 10
    st.markdown('**Evolução da Exportação para os Principais Importadores**')
    #line
    st.plotly_chart(fig_evolucao_quantidade_top_10_line, use_container_width = True)
    #treemap
    st.plotly_chart(fig_evolucao_quantidade_top_10_treemap, use_container_width = True)

with tab3:

    #cartões
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('**Preço Médio**', formata_numero_cartao(dados['valor_exportacao_por_litro'].mean(), 'US$', ''))
    with coluna2:
        st.metric('**Percentual Médio**', formata_numero_cartao(dados['percentual_exportacao'].mean(), '', '\%'))

    coluna3, coluna4 = st.columns(2)
    with coluna3:
        st.metric('**Preço Médio em 2021**', formata_numero_cartao(dados.query('ano == 2021')['valor_exportacao_por_litro'].mean(), 'US$', ''))
    with coluna4:
        st.metric('**Percentual Médio em 2021**', formata_numero_cartao(dados.query('ano == 2021')['percentual_exportacao'].mean(), '', '\%'))

    #evolução do preço médio 
    st.markdown('**Evolução do Preço Médio por Litro**')
    st.plotly_chart(fig_evolucao_preco_medio_por_litro, use_container_width = True) 

    #preço médio top 10
    st.markdown('**Preço Médio por Litro para os Principais Importadores**')
    coluna5, coluna6 = st.columns(2)
    with coluna5:
        #bar
        st.plotly_chart(fig_preco_medio_por_litro_top_10_bar, use_container_width = True)
    with coluna6:
        #treemap
        st.plotly_chart(fig_preco_medio_por_litro_top_10_treemap, use_container_width = True)

    '''
    Vê-se que, nos últimos 15 anos, o comércio com a Rússia e o Haiti apresentaram os piores resultados no acumulado. Já o comércio com o Paraguai, 
    apesar de apresentar o maior resultado absoluto no montate dos valores negociados, é 8° mercado mais rentável do período.'''

    #evolução do preço médio top 10
    st.markdown('**Evolução do Preço por Litro para os Principais Importadores**')
    st.plotly_chart(fig_evolucao_valor_por_litro_top_10, use_container_width = True)

    #evolução do percentual médio 
    st.markdown('**Evolução do Percentual Médio da Produção Nacional Exportado**')
    st.plotly_chart(fig_evolucao_percentual_medio_exportacao, use_container_width = True) 

    #percentual médio top 10
    st.markdown('**Percentual Médio da Produção Nacional para os Principais Importadores**')
    coluna7, coluna8 = st.columns(2)
    with coluna7:
        #bar
        st.plotly_chart(fig_percentual_medio_exportacao_top_10_bar, use_container_width = True)
    with coluna8:
        #treemap
        st.plotly_chart(fig_percentual_medio_exportacao_top_10_treemap, use_container_width = True)

    #evolução do percentual médio top 10
    st.markdown('**Evolução do Percentual Médio da Produção Nacional para os Principais Importadores**')
    st.plotly_chart(fig_evolucao_percentual_medio_exportacao_top_10, use_container_width = True)
  
    #distribuição top 10
    st.markdown('**Distribuição da Quantidade e Valor da Exportação para os Principais Importadores**')
    coluna9, coluna10 = st.columns(2)
    with coluna9:
        st.plotly_chart(fig_distribuicao_valor_top_10, use_container_width = True)
    with coluna10:
        st.plotly_chart(fig_distribuicao_quantidade_top_10, use_container_width = True)

    'Nota-se que a Rússia, apesar de em números absolutos ter uma grande parcela na exportação, não é um mercado regular.'