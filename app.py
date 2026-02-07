import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Plano Rumo ao Milhão - Rico Plus",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado para design premium COM MELHOR CONTRASTE
st.markdown("""
<style>
    /* Fundo gradiente mais suave */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 100%);
    }
    
    /* Cards brancos com sombra */
    .stTabs [data-baseweb="tab-panel"] {
        background-color: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin-top: 1rem;
    }
    
    /* Métricas maiores e com boa legibilidade */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #1e293b !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #475569 !important;
    }
    
    /* Títulos com melhor contraste */
    h1 {
        color: #1e293b !important;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-shadow: 2px 2px 4px rgba(255,255,255,0.8);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        color: #667eea !important;
        font-weight: 700 !important;
    }
    
    h3 {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    /* Abas */
    [data-baseweb="tab-list"] {
        background-color: white;
        border-radius: 15px;
        padding: 0.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    [data-baseweb="tab"] {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #475569 !important;
    }
    
    [aria-selected="true"] {
        color: #667eea !important;
    }
    
    /* Inputs com melhor visibilidade */
    [data-testid="stNumberInput"] input {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #1e293b !important;
    }
    
    /* Labels dos inputs */
    label {
        color: #475569 !important;
        font-weight: 600 !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Texto geral mais escuro */
    p, span, div {
        color: #334155 !important;
    }
    
    /* Success/Info/Warning boxes */
    .stSuccess, .stInfo, .stWarning {
        background-color: white !important;
        border-left: 4px solid #667eea !important;
        color: #1e293b !important;
    }
    
    /* Captions mais legíveis */
    .stCaptionContainer {
        color: #64748b !important;
    }
    
    /* Sliders */
    [data-testid="stSlider"] label {
        color: #475569 !important;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session_state
if 'renda_mensal' not in st.session_state:
    st.session_state.renda_mensal = 10000
if 'anos' not in st.session_state:
    st.session_state.anos = 10
if 'taxa_anual' not in st.session_state:
    st.session_state.taxa_anual = 6.0
if 'patrimonio' not in st.session_state:
    st.session_state.patrimonio = 0
if 'aporte' not in st.session_state:
    st.session_state.aporte = 0
if 'salario' not in st.session_state:
    st.session_state.salario = 6000.00
if 'gastos' not in st.session_state:
    st.session_state.gastos = 4000.00
if 'categorias_gastos' not in st.session_state:
    st.session_state.categorias_gastos = {
        'Moradia': 1500,
        'Alimentação': 800,
        'Transporte': 400,
        'Lazer': 500,
        'Outros': 800
    }

# Título principal
st.title("💰 Plano Rumo ao Milhão")
st.markdown("### ✨ Transforme sua vida financeira com inteligência e disciplina!")
st.markdown("")

# Criar abas
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard", 
    "🎯 Minha Meta", 
    "📈 Projeção", 
    "💎 Onde Investir", 
    "📉 Controle de Gastos"
])

# ==================== ABA 1: DASHBOARD ====================
with tab1:
    st.markdown("## 🎯 Visão Geral Rápida")
    st.markdown("")
    
    # Calcular valores
    sobra = st.session_state.salario - st.session_state.gastos
    patrimonio = st.session_state.renda_mensal * 12 / 0.04
    taxa_mensal = st.session_state.taxa_anual / 100 / 12
    meses = st.session_state.anos * 12
    
    if taxa_mensal > 0:
        aporte = patrimonio * taxa_mensal / ((1 + taxa_mensal)**meses - 1)
    else:
        aporte = patrimonio / meses
    
    st.session_state.patrimonio = patrimonio
    st.session_state.aporte = aporte
    
    # Cards principais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "💵 Sua Sobra Mensal",
            f"R$ {sobra:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            delta="Disponível para investir"
        )
        
    with col2:
        if aporte > 0:
            percentual = (sobra / aporte) * 100
        else:
            percentual = 0
        st.metric(
            "🎯 Meta Atingida",
            f"{percentual:.1f}%",
            delta=f"R$ {sobra - aporte:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        
    with col3:
        rendimento_mensal = sobra * 0.17 / 12  # Melhor taxa (PagBank 130%)
        st.metric(
            "💰 Rendimento Mensal",
            f"R$ {rendimento_mensal:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            delta="Com PagBank 130% CDI"
        )
    
    st.markdown("---")
    
    # Resumo financeiro
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📋 Seu Resumo Financeiro")
        
        dados_resumo = pd.DataFrame({
            'Categoria': ['Salário Líquido', 'Gastos Totais', 'Sobra', 'Aporte Necessário', 'Diferença'],
            'Valor': [
                st.session_state.salario,
                st.session_state.gastos,
                sobra,
                aporte,
                sobra - aporte
            ]
        })
        
        for _, row in dados_resumo.iterrows():
            cor = "🟢" if row['Valor'] > 0 or row['Categoria'] == 'Salário Líquido' else "🔴"
            valor_fmt = f"R$ {abs(row['Valor']):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            if row['Valor'] < 0:
                valor_fmt = f"-{valor_fmt}"
            st.markdown(f"{cor} **{row['Categoria']}**: {valor_fmt}")
    
    with col2:
        st.markdown("### 🎁 Dica do Dia")
        st.info("""
        💡 **Automatize seus investimentos!**
        
        Configure débito automático no dia do pagamento. Assim você:
        - Nunca esquece de investir
        - Evita gastar o dinheiro
        - Aproveita juros compostos desde o dia 1
        """)
    
    st.markdown("---")
    st.markdown("#### 🚀 Comece HOJE | Evite dívidas caras | Revise só 1× por mês")

# ==================== ABA 2: MINHA META ====================
with tab2:
    st.markdown("## 🎯 Defina sua Meta de Independência Financeira")
    st.markdown("")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### ⚙️ Configurações")
        
        st.session_state.renda_mensal = st.number_input(
            "💰 Renda mensal desejada (R$)",
            value=st.session_state.renda_mensal,
            min_value=2000,
            max_value=100000,
            step=500,
            format="%d",
            help="Quanto você quer receber por mês de renda passiva?"
        )
        
        st.session_state.anos = st.slider(
            "⏰ Em quantos anos?",
            min_value=5,
            max_value=30,
            value=st.session_state.anos,
            step=1,
            help="Prazo para atingir sua meta"
        )
        
        st.session_state.taxa_anual = st.slider(
            "📊 Retorno anual esperado (%)",
            min_value=4.0,
            max_value=15.0,
            value=st.session_state.taxa_anual,
            step=0.5,
            help="Taxa de retorno média anual dos investimentos"
        )
        
        st.markdown("")
        st.info("💡 **Regra dos 4%**: Para viver de renda, você precisa de 25x seu custo anual em patrimônio")
    
    # Recalcular
    patrimonio = st.session_state.renda_mensal * 12 / 0.04
    taxa_mensal = st.session_state.taxa_anual / 100 / 12
    meses = st.session_state.anos * 12
    
    if taxa_mensal > 0:
        aporte = patrimonio * taxa_mensal / ((1 + taxa_mensal)**meses - 1)
    else:
        aporte = patrimonio / meses
    
    st.session_state.patrimonio = patrimonio
    st.session_state.aporte = aporte
    
    with col2:
        st.markdown("### 🎯 Seus Números da Liberdade")
        st.markdown("")
        
        st.metric(
            "💎 Patrimônio necessário",
            f"R$ {patrimonio:,.0f}".replace(",", "."),
            help="Valor total que você precisa acumular"
        )
        
        st.metric(
            "📅 Aporte mensal necessário",
            f"R$ {aporte:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            help="Quanto você precisa investir por mês"
        )
        
        st.metric(
            "📈 Total a investir",
            f"R$ {aporte * meses:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            help="Soma de todos os aportes ao longo do tempo"
        )
        
        rendimento_total = patrimonio - (aporte * meses)
        st.metric(
            "🌟 Ganho com juros",
            f"R$ {rendimento_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            delta=f"{(rendimento_total/(aporte * meses)*100):.1f}% de ganho",
            help="Quanto os juros compostos vão render"
        )
        
        st.markdown("")
        st.success(f"🎯 Em **{st.session_state.anos} anos** você terá **R$ {st.session_state.renda_mensal:,.0f}/mês** de renda passiva!".replace(",", "."))
    
    st.markdown("---")
    
    # Comparação com trabalho
    st.markdown("### 💼 Comparação: Trabalhar vs Investir")
    
    anos_trabalhando = st.session_state.renda_mensal * 12 * st.session_state.anos
    ganho_investindo = rendimento_total
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        **Trabalhando {st.session_state.anos} anos:**
        - Receberá: R$ {anos_trabalhando:,.2f}
        - Depois: precisa continuar trabalhando
        - Liberdade: ❌
        """.replace(",", "X").replace(".", ",").replace("X", "."))
    
    with col2:
        st.markdown(f"""
        **Investindo {st.session_state.anos} anos:**
        - Investirá: R$ {aporte * meses:,.2f}
        - Ganhará de juros: R$ {rendimento_total:,.2f}
        - Depois: vive de renda para sempre ✅
        - Liberdade: ✅✅✅
        """.replace(",", "X").replace(".", ",").replace("X", "."))
    
    st.markdown("---")
    st.markdown("#### 🚀 Comece HOJE | Evite dívidas caras | Revise só 1× por mês")

# ==================== ABA 3: PROJEÇÃO ====================
with tab3:
    st.markdown("## 📈 Visualize seu Crescimento Patrimonial")
    st.markdown("")
    
    patrimonio_meta = st.session_state.patrimonio
    aporte_mensal = st.session_state.aporte
    anos_meta = st.session_state.anos
    taxa_anual_meta = st.session_state.taxa_anual
    taxa_mensal_calc = taxa_anual_meta / 100 / 12
    
    # Criar dados ano a ano
    anos_lista = np.arange(0, anos_meta + 1)
    patrimonio_acumulado = []
    total_investido_lista = []
    juros_acumulados = []
    
    for ano in anos_lista:
        meses_total = ano * 12
        if taxa_mensal_calc > 0 and meses_total > 0:
            total = aporte_mensal * (((1 + taxa_mensal_calc)**meses_total - 1) / taxa_mensal_calc)
        else:
            total = 0
        patrimonio_acumulado.append(total)
        investido = aporte_mensal * meses_total
        total_investido_lista.append(investido)
        juros_acumulados.append(total - investido)
    
    # DataFrame para gráfico
    df_projecao = pd.DataFrame({
        'Ano': anos_lista,
        'Patrimônio Total': patrimonio_acumulado,
        'Investido': total_investido_lista,
        'Juros': juros_acumulados
    })
    
    # Gráfico de área empilhada
    df_melted = df_projecao.melt('Ano', var_name='Tipo', value_name='Valor')
    df_melted = df_melted[df_melted['Tipo'] != 'Patrimônio Total']
    
    chart = alt.Chart(df_melted).mark_area(opacity=0.7).encode(
        x=alt.X('Ano:Q', title='Anos'),
        y=alt.Y('Valor:Q', title='Valor (R$)', axis=alt.Axis(format=',.0f')),
        color=alt.Color('Tipo:N', 
            scale=alt.Scale(domain=['Investido', 'Juros'], 
                          range=['#667eea', '#f093fb']),
            legend=alt.Legend(title="Composição")
        ),
        tooltip=[
            alt.Tooltip('Ano:Q', title='Ano'),
            alt.Tooltip('Tipo:N', title='Tipo'),
            alt.Tooltip('Valor:Q', title='Valor', format=',.2f')
        ]
    ).properties(
        width=800,
        height=450,
        title=f'Evolução do Patrimônio em {anos_meta} anos'
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    st.markdown("---")
    
    # Métricas finais
    col1, col2, col3, col4 = st.columns(4)
    
    total_investido = aporte_mensal * anos_meta * 12
    ganho_juros = patrimonio_acumulado[-1] - total_investido
    
    with col1:
        st.metric("💵 Total Investido", f"R$ {total_investido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    with col2:
        st.metric("🌟 Ganho com Juros", f"R$ {ganho_juros:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    with col3:
        percentual_ganho = (ganho_juros / total_investido * 100) if total_investido > 0 else 0
        st.metric("📊 Ganho %", f"{percentual_ganho:.1f}%")
    
    with col4:
        st.metric("💎 Patrimônio Final", f"R$ {patrimonio_acumulado[-1]:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    st.markdown("---")
    
    # Tabela ano a ano
    with st.expander("📋 Ver detalhamento ano a ano"):
        df_display = df_projecao.copy()
        df_display['Ano'] = df_display['Ano'].astype(int)
        df_display['Patrimônio Total'] = df_display['Patrimônio Total'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        df_display['Investido'] = df_display['Investido'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        df_display['Juros'] = df_display['Juros'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.dataframe(df_display, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### 🚀 Comece HOJE | Evite dívidas caras | Revise só 1× por mês")

# ==================== ABA 4: ONDE INVESTIR ====================
with tab4:
    st.markdown("## 💎 Onde Aplicar sua Sobra Hoje? (Fevereiro 2026)")
    st.caption("📌 **CDI/Selic ≈ 14,9% a.a.** | Todos com FGC até R$ 250 mil")
    st.markdown("")
    
    # Inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.salario = st.number_input(
            "💰 Salário líquido (R$)",
            value=st.session_state.salario,
            min_value=0.00,
            step=100.00,
            format="%.2f"
        )
        
    with col2:
        st.session_state.gastos = st.number_input(
            "💳 Gastos mensais (R$)",
            value=st.session_state.gastos,
            min_value=0.00,
            step=100.00,
            format="%.2f"
        )
    
    sobra = st.session_state.salario - st.session_state.gastos
    aporte_necessario = st.session_state.aporte
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "💵 Sobra para Investir",
            f"R$ {sobra:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            delta="Disponível agora"
        )
    
    with col2:
        if aporte_necessario > 0:
            percentual = (sobra / aporte_necessario) * 100
        else:
            percentual = 0
        st.metric(
            "🎯 Meta Atingida",
            f"{percentual:.1f}%"
        )
    
    with col3:
        melhor_rend = sobra * 0.193 / 12  # Nubank Turbo 120% CDI
        st.metric(
            "🚀 Melhor Rendimento",
            f"R$ {melhor_rend:,.2f}/mês".replace(",", "X").replace(".", ",").replace("X", "."),
            delta="Nubank Turbo"
        )
    
    st.markdown("### 📊 Progresso em relação ao aporte necessário")
    if aporte_necessario > 0 and sobra > 0:
        progress_value = min(sobra / aporte_necessario, 1.0)
    else:
        progress_value = 0.0
    st.progress(progress_value)
    
    st.markdown("---")
    st.markdown("### 🏦 Melhores Opções de Investimento")
    st.markdown("")
    
    # Lista de investimentos com dados reais
    investimentos = [
        {
            'nome': 'Nubank Caixinhas Turbo',
            'emoji': '🟣',
            'taxa': 120.0,  # % do CDI
            'cdi_aa': 14.9,
            'destaque': True,
            'obs': '⚡ PROMOÇÃO! Limitado a R$ 3.000'
        },
        {
            'nome': 'Nubank Caixinha',
            'emoji': '🟣',
            'taxa': 100.0,
            'cdi_aa': 14.9,
            'destaque': False,
            'obs': 'Liquidez diária'
        },
        {
            'nome': 'PagBank',
            'emoji': '🔵',
            'taxa': 130.0,
            'cdi_aa': 14.9,
            'destaque': True,
            'obs': '🔥 Maior taxa! Promoção'
        },
        {
            'nome': 'Banco Inter',
            'emoji': '🟠',
            'taxa': 102.0,
            'cdi_aa': 14.9,
            'destaque': False,
            'obs': 'Confiável e estável'
        },
        {
            'nome': 'C6 Bank',
            'emoji': '⚫',
            'taxa': 104.0,
            'cdi_aa': 14.9,
            'destaque': False,
            'obs': 'Boa opção'
        },
        {
            'nome': 'PicPay',
            'emoji': '🟢',
            'taxa': 105.0,
            'cdi_aa': 14.9,
            'destaque': False,
            'obs': 'Fácil de usar'
        },
        {
            'nome': 'BTG Pactual',
            'emoji': '⚪',
            'taxa': 104.0,
            'cdi_aa': 14.9,
            'destaque': False,
            'obs': 'Banco de investimentos'
        },
        {
            'nome': 'Santander',
            'emoji': '🔴',
            'taxa': 101.0,
            'cdi_aa': 14.9,
            'destaque': False,
            'obs': 'Banco tradicional'
        },
        {
            'nome': 'Tesouro Selic',
            'emoji': '🏛️',
            'taxa': 100.0,
            'cdi_aa': 14.9,
            'destaque': False,
            'obs': 'Mais seguro (Governo)'
        }
    ]
    
    # Ordenar por taxa
    investimentos_sorted = sorted(investimentos, key=lambda x: x['taxa'], reverse=True)
    
    # Exibir cards
    for i in range(0, len(investimentos_sorted), 2):
        col1, col2 = st.columns(2)
        
        for j, col in enumerate([col1, col2]):
            if i + j < len(investimentos_sorted):
                inv = investimentos_sorted[i + j]
                taxa_aa = inv['taxa'] / 100 * inv['cdi_aa']
                rendimento = sobra * (taxa_aa / 100) / 12
                
                with col:
                    if inv['destaque']:
                        st.markdown(f"### {inv['emoji']} {inv['nome']} ⭐")
                    else:
                        st.markdown(f"### {inv['emoji']} {inv['nome']}")
                    
                    st.markdown(f"**{inv['taxa']:.0f}% CDI** (~{taxa_aa:.1f}% a.a.)")
                    st.caption(f"💰 Rende ≈ **R$ {rendimento:,.2f}** por mês".replace(",", "X").replace(".", ",").replace("X", "."))
                    st.caption(f"📝 {inv['obs']}")
                    
                    if inv['destaque']:
                        st.success("✅ Recomendado!")
        
        st.markdown("---")
    
    # Comparação visual
    st.markdown("### 📊 Comparação de Rendimentos (com sua sobra)")
    
    df_comparacao = pd.DataFrame([
        {
            'Banco': inv['nome'],
            'Rendimento Mensal': sobra * (inv['taxa'] / 100 * inv['cdi_aa'] / 100) / 12
        }
        for inv in investimentos_sorted[:6]  # Top 6
    ])
    
    chart_comp = alt.Chart(df_comparacao).mark_bar().encode(
        x=alt.X('Rendimento Mensal:Q', title='Rendimento Mensal (R$)', axis=alt.Axis(format=',.2f')),
        y=alt.Y('Banco:N', title='', sort='-x'),
        color=alt.Color('Rendimento Mensal:Q', scale=alt.Scale(scheme='viridis'), legend=None),
        tooltip=[
            alt.Tooltip('Banco:N'),
            alt.Tooltip('Rendimento Mensal:Q', title='Rendimento', format=',.2f')
        ]
    ).properties(
        height=300
    )
    
    st.altair_chart(chart_comp, use_container_width=True)
    
    st.markdown("---")
    
    # Recomendação final
    st.success("""
    ✅ **Estratégia Recomendada:**
    
    1. **Nubank Turbo** (120% CDI) → Até R$ 3.000 (aproveite a promoção!)
    2. **PagBank** (130% CDI) → Restante da sobra
    3. Depois diversifique: Inter, C6, BTG
    4. Tesouro Selic para segurança máxima
    
    💡 **Dica Pro**: Diversifique em 3-4 bancos para maximizar o FGC (R$ 250k por instituição)
    """)
    
    st.markdown("---")
    st.markdown("#### 🚀 Comece HOJE | Evite dívidas caras | Revise só 1× por mês")

# ==================== ABA 5: CONTROLE DE GASTOS ====================
with tab5:
    st.markdown("## 📉 Controle de Gastos e Otimização")
    st.markdown("")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 💳 Suas Categorias de Gastos")
        
        total_categorias = 0
        for categoria, valor in st.session_state.categorias_gastos.items():
            novo_valor = st.number_input(
                f"{categoria}",
                value=float(valor),
                min_value=0.0,
                step=50.0,
                format="%.2f",
                key=f"cat_{categoria}"
            )
            st.session_state.categorias_gastos[categoria] = novo_valor
            total_categorias += novo_valor
        
        st.markdown("---")
        st.metric("💰 Total de Gastos", f"R$ {total_categorias:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        
        diferenca = st.session_state.gastos - total_categorias
        if abs(diferenca) > 0.01:
            st.warning(f"⚠️ Diferença de R$ {diferenca:,.2f} em relação ao total declarado".replace(",", "X").replace(".", ",").replace("X", "."))
    
    with col2:
        st.markdown("### 📊 Distribuição dos Gastos")
        
        df_gastos = pd.DataFrame({
            'Categoria': list(st.session_state.categorias_gastos.keys()),
            'Valor': list(st.session_state.categorias_gastos.values())
        })
        
        chart_pizza = alt.Chart(df_gastos).mark_arc(innerRadius=50).encode(
            theta=alt.Theta('Valor:Q'),
            color=alt.Color('Categoria:N', scale=alt.Scale(scheme='tableau10')),
            tooltip=[
                alt.Tooltip('Categoria:N'),
                alt.Tooltip('Valor:Q', title='Valor', format=',.2f')
            ]
        ).properties(
            height=350
        )
        
        st.altair_chart(chart_pizza, use_container_width=True)
    
    st.markdown("---")
    
    # Análise e dicas
    st.markdown("### 💡 Análise e Dicas de Otimização")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔴 Onde Cortar Gastos?")
        
        # Identificar maior gasto
        maior_cat = max(st.session_state.categorias_gastos, key=st.session_state.categorias_gastos.get)
        maior_valor = st.session_state.categorias_gastos[maior_cat]
        perc_maior = (maior_valor / total_categorias * 100) if total_categorias > 0 else 0
        
        st.warning(f"""
        Sua maior despesa é **{maior_cat}**: R$ {maior_valor:,.2f} ({perc_maior:.1f}%)
        
        **Dicas para reduzir:**
        """.replace(",", "X").replace(".", ",").replace("X", "."))
        
        dicas_economia = {
            'Moradia': [
                "🏠 Considere dividir apartamento",
                "💡 Reduza conta de luz (LED, ar-condicionado)",
                "💧 Economize água"
            ],
            'Alimentação': [
                "🍳 Cozinhe em casa (75% mais barato)",
                "🛒 Compre no atacado",
                "📦 Use apps de cashback"
            ],
            'Transporte': [
                "🚇 Use transporte público",
                "🚴 Bicicleta para trajetos curtos",
                "🚗 Carona compartilhada"
            ],
            'Lazer': [
                "🎬 Streamings compartilhados",
                "🌳 Atividades gratuitas ao ar livre",
                "📚 Biblioteca pública"
            ],
            'Outros': [
                "✂️ Cancele assinaturas não usadas",
                "📱 Revise plano de celular",
                "🛍️ Evite compras por impulso"
            ]
        }
        
        for dica in dicas_economia.get(maior_cat, ["Revise seus gastos"]):
            st.markdown(f"- {dica}")
    
    with col2:
        st.markdown("#### 🟢 Como Aumentar sua Sobra?")
        
        meta_economia = st.slider(
            "Meta de economia (%)",
            min_value=5,
            max_value=30,
            value=10,
            step=5,
            help="Quanto % quer economizar dos gastos atuais?"
        )
        
        economia_mensal = total_categorias * (meta_economia / 100)
        nova_sobra = sobra + economia_mensal
        
        st.success(f"""
        Com **{meta_economia}%** de economia:
        
        - Economizará: **R$ {economia_mensal:,.2f}/mês**
        - Nova sobra: **R$ {nova_sobra:,.2f}/mês**
        - Extra por ano: **R$ {economia_mensal * 12:,.2f}**
        """.replace(",", "X").replace(".", ",").replace("X", "."))
        
        # Comparar com meta
        if aporte_necessario > 0:
            novo_perc = (nova_sobra / aporte_necessario) * 100
            st.metric(
                "🎯 Nova % da Meta",
                f"{novo_perc:.1f}%",
                delta=f"+{novo_perc - percentual:.1f}%"
            )
    
    st.markdown("---")
    
    # Desafios
    st.markdown("### 🏆 Desafios de Economia")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **Desafio 30 dias sem delivery**
        
        💰 Economia estimada: R$ 500
        📅 Duração: 1 mês
        🎯 Dificuldade: Média
        """)
    
    with col2:
        st.info("""
        **Desafio cancelar assinaturas**
        
        💰 Economia estimada: R$ 200
        📅 Duração: Permanente
        🎯 Dificuldade: Fácil
        """)
    
    with col3:
        st.info("""
        **Desafio transporte alternativo**
        
        💰 Economia estimada: R$ 300
        📅 Duração: Contínuo
        🎯 Dificuldade: Média
        """)
    
    st.markdown("---")
    st.markdown("#### 🚀 Comece HOJE | Evite dívidas caras | Revise só 1× por mês")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: white; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);'>
    <h2 style='color: #667eea; margin-bottom: 1rem;'>💎 Plano Rumo ao Milhão</h2>
    <p style='font-size: 1.1rem; color: #475569; margin-bottom: 0.5rem;'>
        Ferramenta desenvolvida por <strong style='color: #667eea;'>Rico Plus</strong>
    </p>
    <p style='font-size: 1rem; color: #64748b;'>
        🌐 <a href='https://www.ricoplus.com.br' target='_blank' style='color: #667eea; text-decoration: none; font-weight: 600;'>www.ricoplus.com.br</a>
    </p>
    <p style='font-size: 0.95rem; color: #94a3b8; font-style: italic; margin-top: 1rem;'>
        "O melhor momento para investir foi há 10 anos. O segundo melhor momento é agora."
    </p>
</div>
""", unsafe_allow_html=True)