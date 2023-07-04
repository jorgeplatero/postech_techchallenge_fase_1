#para rodar a aplicação: python -m streamlit run app.py

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

#theme
base = 'dark'

#lendo a base de dados
dados = pd.read_csv('dados_uteis.csv')

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
        st.metric('Valor Total', formata_numero_cartao(dados['valor_exportacao'].sum(), 'US$'))
    with coluna2:
        st.metric('Valor Total em 2021', formata_numero_cartao(dados.query('ano == 2021')['valor_exportacao'].sum(), ''))
    
    #evolução dos valores exportados
    st.markdown('Evolução dos Valores Negociados')
    evolucao_exportacao = dados.groupby('ano').sum().drop('pais', axis = 1)
    fig1 = px.line(
    evolucao_exportacao, 
    x = evolucao_exportacao.index, 
    y = 'valor_exportacao',
    color_discrete_sequence = ['#673E69']
    )
    fig1.update_layout(
        title = '', 
        xaxis_title = 'Período', 
        yaxis_title = 'Valor (US$)', 
        showlegend = False, 
        height = 600
        )
    st.plotly_chart(fig1, use_container_width = True)

    #acumulado valor
    st.markdown('Acumulado dos Valores para os Principais Importadores')
    coluna3, coluna4 = st.columns(2)
    with coluna3:
        #bar
        acumulado_top_10_mercados = pd.DataFrame(dados.groupby('pais').sum()[['quantidade_exportacao', 'valor_exportacao']])
        selecao = acumulado_top_10_mercados.sort_values('valor_exportacao', ascending = False).head(10).index #selecionando os 10 maiores mercados de exportação
        acumulado_top_10_mercados = acumulado_top_10_mercados.loc[selecao]
        acumulado_top_10_mercados.reset_index(inplace = True)
        fig2 = px.bar(
        data_frame = acumulado_top_10_mercados,
        x = 'pais',
        y = 'valor_exportacao',
        color_discrete_sequence = ['#673E69']
        )
        fig2.update_layout(
            title = 'Bar', 
            xaxis_title = 'Países', 
            yaxis_title = 'Valor (US$)', 
            showlegend = False, 
            height = 600, 
            bargap = 0.1
            )
        st.plotly_chart(fig2, use_container_width = True)
    with coluna4:
        #treemap
        fig3 = px.treemap(acumulado_top_10_mercados, path = ['pais'], values = 'valor_exportacao', title = 'Treemap', height = 600)
        fig3.update_traces(root_color = '#673E69')
        st.plotly_chart(fig3, use_container_width = True)

    #evolução de valores exportados top 10
    st.markdown('Evolução dos Valores para os Principais Importadores')
    selecao = acumulado_top_10_mercados['pais'].to_list()
    evolucao_top_10 = dados[dados.pais.isin(selecao)]
    #line
    fig4 = px.line(
    data_frame = evolucao_top_10, 
    x = 'ano', 
    y = 'valor_exportacao',
    color = 'pais'
    )
    fig4.update_layout(
        title = 'Time series', 
        xaxis_title = 'Período', 
        yaxis_title = 'Valor (US$)', 
        legend_title = 'Legenda',
        height = 600
        )
    st.plotly_chart(fig4, use_container_width = True)
    #treemap
    fig5 = px.treemap(evolucao_top_10, path = ['ano', 'pais'], values = 'valor_exportacao', title = 'Treemap', height = 600)
    fig5.update_traces(root_color = '#673E69')
    st.plotly_chart(fig5, use_container_width = True)

with tab2:

    #cartões
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Quantidade Total', formata_numero_cartao(dados['quantidade_exportacao'].sum(), '', 'de litros'))
    with coluna2:
        st.metric('Quantidade Total em 2021', formata_numero_cartao(dados.query('ano == 2021')['quantidade_exportacao'].sum(), '', 'de litros'))
    
    #evolução da quantidade exportada
    st.markdown('Evolução da Quantidade Negociada')
    evolucao_exportacao = dados.groupby('ano').sum().drop('pais', axis = 1)
    fig1 = px.line(
    evolucao_exportacao, 
    x = evolucao_exportacao.index, 
    y = 'quantidade_exportacao',
    color_discrete_sequence = ['#D8D87C']
    )
    fig1.update_layout(
        title = '', 
        xaxis_title = 'Países', 
        yaxis_title = 'Quantidade (Litros)', 
        showlegend = False, 
        height = 600
        )
    st.plotly_chart(fig1, use_container_width = True)

    #acumulado quantidade
    st.markdown('Acumulado da Exportação para os Principais Importadores')
    coluna3, coluna4 = st.columns(2)
    with coluna3:
        #bar 
        fig2 = px.bar(
        data_frame = acumulado_top_10_mercados,
        x = 'pais',
        y = 'quantidade_exportacao',
        color_discrete_sequence = ['#D8D87C']
        )
        fig2.update_layout(
            title = 'Bar', 
            xaxis_title = 'Países', 
            yaxis_title = 'Valor (US$)', 
            showlegend = False, 
            height = 600, 
            bargap = 0.1
            )
        st.plotly_chart(fig2, use_container_width = True)
    with coluna4:
        #treemap
        fig3 = px.treemap(acumulado_top_10_mercados, path = ['pais'], values = 'quantidade_exportacao', title = 'Treemap', height = 600)
        fig3.update_traces(root_color = '#D8D87C')
        st.plotly_chart(fig3, use_container_width = True)
    
    #evolução da quantidade exportada top 10
    st.markdown('Evolução da Exportação para os Principais Importadores')
    #line
    fig4 = px.line(
    data_frame = evolucao_top_10, 
    x = 'ano', 
    y = 'quantidade_exportacao',
    color = 'pais'
    )
    fig4.update_layout(
        title = 'Time series', 
        xaxis_title = 'Período', 
        yaxis_title = 'Quantidade (Litros)', 
        legend_title = 'Legenda',
        height = 600
        )
    st.plotly_chart(fig4, use_container_width = True)
    #treemap
    fig4 = px.treemap(evolucao_top_10, path = ['ano', 'pais'], values = 'quantidade_exportacao', title = 'Treemap', height = 600)
    fig4.update_traces(root_color = '#D8D87C')
    st.plotly_chart(fig4, use_container_width = True)

with tab3:

    #cartões
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Preço Médio', formata_numero_cartao(dados['valor_exportacao_por_litro'].mean(), 'US$', ''))
    with coluna2:
        st.metric('Percentual Médio', formata_numero_cartao(dados['percentual_exportacao'].mean(), '', '\%'))

    coluna3, coluna4 = st.columns(2)
    with coluna3:
        st.metric('Preço Médio em 2021', formata_numero_cartao(dados.query('ano == 2021')['valor_exportacao_por_litro'].mean(), 'US$', ''))
    with coluna4:
        st.metric('Percentual Médio em 2021', formata_numero_cartao(dados.query('ano == 2021')['percentual_exportacao'].mean(), '', '\%'))

    #evolução do preço médio 
    st.markdown('Evolução do Preço Médio por Litro')
    evolucao_preco_medio_por_litro = dados.groupby('ano').mean('valor_exportacao_por_litro').round(2)
    fig1 = px.line(
        data_frame = evolucao_preco_medio_por_litro, 
        x = evolucao_preco_medio_por_litro.index, 
        y = 'valor_exportacao_por_litro',
        color_discrete_sequence = ['#673E69']
    )
    fig1.update_layout(
        title = 'Time series', 
        xaxis_title = 'Período', 
        yaxis_title = 'Valor (US$$)',
        height = 600
        )
    st.plotly_chart(fig1, use_container_width = True) 

    #preço médio top 10
    st.markdown('Preço Médio por Litro para os Principais Importadores')
    coluna5, coluna6 = st.columns(2)
    with coluna5:
        #bar
        preco_medio_por_litro_top_10 = evolucao_top_10[['pais', 'valor_exportacao_por_litro']].groupby('pais').mean().round(2)
        fig2 = px.bar(
            data_frame = preco_medio_por_litro_top_10, 
            x = preco_medio_por_litro_top_10.index, 
            y = 'valor_exportacao_por_litro',
            color_discrete_sequence = ['#673E69']
        )
        fig2.update_layout(
            title = 'Time series', 
            xaxis_title = 'Países', 
            yaxis_title = 'Valor (US$)', 
            height = 600,
            bargap = 0.1
            )
        st.plotly_chart(fig2, use_container_width = True)
    with coluna6:
        #treemap
        fig3 = px.treemap(preco_medio_por_litro_top_10, path = [preco_medio_por_litro_top_10.index], values = 'valor_exportacao_por_litro', title = 'Treemap', height = 600)
        fig3.update_traces(root_color = '#673E69')
        st.plotly_chart(fig3, use_container_width = True)

    #evolução do preço médio top 10
    st.markdown('Evolução do Preço por Litro para os Principais Importadores')
    fig4 = px.line(
    data_frame = evolucao_top_10, 
    x = 'ano', 
    y = 'valor_exportacao_por_litro',
    color = 'pais'
    )
    fig4.update_layout(
        title = 'Time series', 
        xaxis_title = 'Período', 
        yaxis_title = 'Valor (US$)', 
        legend_title = 'Legenda',
        height = 600
        )
    st.plotly_chart(fig4, use_container_width = True)

    #evolução do percentual médio 
    st.markdown('Evolução do Percentual Médio da Produção Nacional Exportado')
    percentual_exportacao = dados[['ano', 'pais', 'percentual_exportacao']].round(2)
    evolucao_percentual_medio_exportacao = percentual_exportacao.groupby('ano').mean('percentual_exportacao').round(2)
    fig5 = px.line(
        data_frame = evolucao_percentual_medio_exportacao, 
        x = evolucao_percentual_medio_exportacao.index, 
        y = 'percentual_exportacao',
        color_discrete_sequence = ['#673E69']
    )
    fig5.update_layout(
        title = 'Time series', 
        xaxis_title = 'Período', 
        yaxis_title = '%',
        height = 600
        )
    st.plotly_chart(fig5, use_container_width = True) 

    #percentual médio top 10
    st.markdown('Percentual Médio da Produção Nacional para os Principais Importadores')
    coluna7, coluna8 = st.columns(2)
    with coluna7:
        #bar
        percentual_medio_exportacao_top_10 = evolucao_top_10.groupby('pais').mean('percentual_exportacao').round(2)
        fig6 = px.bar(
            data_frame = percentual_medio_exportacao_top_10, 
            x = percentual_medio_exportacao_top_10.index, 
            y = 'percentual_exportacao',
            color_discrete_sequence = ['#673E69']
        )
        fig6.update_layout(
            title = 'Time series', 
            xaxis_title = 'Países', 
            yaxis_title = '%', 
            height = 600,
            bargap = 0.1
            )
        st.plotly_chart(fig6, use_container_width = True)
    with coluna8:
        #treemap
        fig7 = px.treemap(percentual_medio_exportacao_top_10, path = [percentual_medio_exportacao_top_10.index], values = 'percentual_exportacao', title = 'Treemap', height = 600)
        fig7.update_traces(root_color = '#673E69')
        st.plotly_chart(fig7, use_container_width = True)

    #evolução do percentual médio top 10
    st.markdown('Evolução do Percentual Médio da Produção Nacional para os Principais Importadores')
    fig8 = px.line(
    data_frame = evolucao_top_10, 
    x = 'ano', 
    y = 'percentual_exportacao',
    color = 'pais'
    )
    fig8.update_layout(
        title = 'Time series', 
        xaxis_title = 'Período', 
        yaxis_title = '%', 
        legend_title = 'Legenda',
        height = 600
        )
    st.plotly_chart(fig8, use_container_width = True)
  
    #distribuição top 10
    st.markdown('Distribuição da Quantidade e Valor da Exportação para os Principais Importadores')
    index = evolucao_top_10.query('quantidade_exportacao == 0').index.to_list()
    distribuicao_top_10 = evolucao_top_10.drop(index)
    distribuicao_top_10.head()
    coluna9, coluna10 = st.columns(2)
    with coluna9:
        fig9 = px.scatter(
            data_frame = distribuicao_top_10, 
            x = 'pais', 
            y = 'ano', 
            size = 'valor_exportacao', 
            color = px.Constant('Valor (US$)'),
            color_discrete_sequence = ['#673E69']
            )
        fig9.update_layout(
            title = 'Bubble', 
            xaxis_title = 'Países', 
            yaxis_title = 'Ano', 
            legend_title = 'Legenda',
            height = 700
            )
        fig9.update_traces(marker = dict(size = 3.5 * distribuicao_top_10['valor_exportacao']))
        st.plotly_chart(fig9, use_container_width = True)
    with coluna10:
        fig10 = px.scatter(
            data_frame = distribuicao_top_10, 
            x = 'pais', 
            y = 'ano', 
            size = 'quantidade_exportacao', 
            color = px.Constant('Quantidade (Litros)'),
            color_discrete_sequence = ['#D8D87C'])
        fig10.update_layout(
            title = 'Bubble', 
            xaxis_title = 'Países', 
            yaxis_title = 'Ano', 
            legend_title = 'Legenda',
            height = 700
            )
        fig10.update_traces(marker = dict(size = 3.5 * distribuicao_top_10['quantidade_exportacao']))
        st.plotly_chart(fig10, use_container_width = True)