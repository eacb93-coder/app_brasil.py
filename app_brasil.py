import streamlit as st
import pandas as pd
from datetime import datetime, time, timedelta

# ==============================================================================
# 1. CONFIGURAÇÃO (MODO ONLINE - GOOGLE SHEETS) ☁️
# ==============================================================================
st.set_page_config(page_title="Gestor de Locadora BR", page_icon="🇧🇷", layout="wide")

# SEU LINK JÁ ESTÁ AQUI 👇
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR2Fjc9qA470SDT12L-_nNlryhKLXHZWXSYPzg-ycg-DGkt_O7suDDtUF3rQEE-pg/pub?gid=858361345&single=true&output=csv"

LOCAIS = {
    "Loja Centro": 0.0,
    "Aeroporto (Taxa Entrega)": 80.00,
    "Hotel / Delivery": 50.00
}

# ==============================================================================
# 2. MOTOR DE DADOS (CONEXÃO EM TEMPO REAL)
# ==============================================================================
# ttl=0 significa ZERO Cache. Atualiza na hora (F5).
@st.cache_data(ttl=0)
def load_data():
    try:
        # O Pandas lê direto do seu link
        df = pd.read_csv(SHEET_URL)
        
        # Limpeza de segurança (remove linhas vazias da planilha)
        df = df.dropna(how='all')
        
        # Verifica se as colunas essenciais existem
        colunas_obrigatorias = ['Carro', 'Preço Baixa', 'Disponibilidade']
        if not all(col in df.columns for col in colunas_obrigatorias):
            st.error("⚠️ Erro: As colunas da planilha não conferem. Verifique o cabeçalho.")
            return pd.DataFrame()
            
        return df
    except Exception as e:
        st.error(f"❌ Erro de Conexão com Google Sheets: {e}")
        return pd.DataFrame()

df = load_data()

def get_car_details(row):
    return {
        "nome": row['Carro'],
        "grupo": row.get('Grupo', 'N/A'),
        "motor": row.get('Motor', '1.0'),
        "cambio": row.get('Câmbio', 'Manual'),
        "p_baixa": row.get('Preço Baixa', 0),
        "p_alta": row.get('Preço Alta', 0),
        "status": str(row.get('Disponibilidade', ''))
    }

# ==============================================================================
# 3. INTELIGÊNCIA DE VENDAS (Script Sazonal) 🧠
# ==============================================================================
def get_script_venda(data_inicio):
    m, d = data_inicio.month, data_inicio.day
    
    # 🎆 REVEILLON
    if (m == 12 and d >= 20) or (m == 1 and d <= 5):
        return {
            "periodo": "🔥 ALTA TEMPORADA (Fim de Ano)",
            "texto": """Olá! Agradecemos o contato.
Infelizmente, o modelo econômico básico já está **ESGOTADO** para o Reveillon.
Mas consegui segurar estas opções superiores:
🚗 **Chevrolet Onix Turbo (Automático)** - Conforto no trânsito.
🚙 **Jeep Renegade Turbo (SUV)** - Status e Espaço.
⚠️ A frota deve zerar em 24h. Recomendo garantir agora."""
        }

    # 🎉 FÉRIAS
    elif m in [2, 3, 7]:
        return {
            "periodo": "⛱️ ALTA TEMPORADA (Férias)",
            "texto": """Olá! O carro popular promocional acabou de sair.
Mas tenho um upgrade com ótimo custo-benefício:
🚗 **Hyundai HB20** - Mais espaço para malas.
🚗 **Chevrolet Onix Turbo** - Wi-Fi e Automático.
Vale muito a pena o conforto extra na viagem!"""
        }

    # 💼 BAIXA (Padrão)
    else:
        return {
            "periodo": "📉 BAIXA TEMPORADA",
            "texto": """Olá! O promocional de entrada não está disponível.
Mas trago boas notícias: estamos com condições especiais em categorias acima:
🚗 **Hyundai HB20** - Por uma pequena diferença, muito mais carro.
🚗 **Onix Turbo** - Economia e Potência.
Posso reservar o HB20? É o nosso campeão de vendas."""
        }

# ==============================================================================
# 4. INTERFACE VISUAL
# ==============================================================================
st.title("🚗 Gestor de Locadora Brasil")
st.caption(f"Status do Sistema: 🟢 Conectado ao Google Sheets (Online)")

if not df.empty:
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("1. Seleção do Veículo")
        carro_selecionado = st.selectbox("Escolha o Carro Solicitado", df['Carro'].tolist())
        
        linha = df[df['Carro'] == carro_selecionado].iloc[0]
        carro = get_car_details(linha)
        
        # --- DETECTOR DE ISCA ---
        e_isca = False
        # Converte para número caso venha como texto do Sheets
        preco_atual = float(str(carro['p_baixa']).replace('R$', '').replace(',', '.'))
        
        if preco_atual <= 100 or "Isca" in carro['status']:
            e_isca = True
            st.error(f"🎣 CARRO ISCA DETECTADO: {carro['nome']}")
            st.info("Script de Upsell Ativado Automaticamente.")
        
        with st.container(border=True):
            c1, c2 = st.columns(2)
            c1.metric("Grupo", carro['grupo'])
            c2.metric("Motor", carro['motor'])
            st.text(f"Câmbio: {carro['cambio']}")
            
            if "ESGOTADO" in carro['status']:
                st.warning(f"Status: {carro['status']}")
            else:
                st.success(f"Status: {carro['status']}")

    with col2:
        st.subheader("2. Dados da Reserva")
        c_a, c_b = st.columns(2)
        with c_a: d_inicio = st.date_input("Retirada", datetime.today())
        with c_b: d_fim = st.date_input("Devolução", datetime.today() + timedelta(days=3))
        local_ret = st.selectbox("Local", list(LOCAIS.keys()))
        
        if st.button("Gerar Orçamento 🚀", type="primary"):
            dt_inicio = datetime.combine(d_inicio, time(10))
            taxa_entrega = LOCAIS[local_ret]
            dias = max((d_fim - d_inicio).days, 1)
            
            if e_isca:
                dados_script = get_script_venda(dt_inicio)
                st.success(f"✅ Estratégia: {dados_script['periodo']}")
                email_final = f"Assunto: Retorno sobre {carro['nome']}\n\n{dados_script['texto']}\n\n✅ INCLUSO: Km Livre, Seguro CDW."
            else:
                is_alta = d_inicio.month in [1, 2, 7, 12]
                p_dia = carro['p_alta'] if is_alta else carro['p_baixa']
                total = (dias * p_dia) + taxa_entrega
                email_final = f"Assunto: Confirmação {carro['nome']}\n\n📋 RESUMO:\n• {dias} dias x R$ {p_dia}\n• Taxa: R$ {taxa_entrega}\n💰 TOTAL: R$ {total:.2f}"

            st.text_area("Copiar E-mail:", email_final, height=400)

else:
    st.warning("⚠️ Carregando dados da nuvem... (Se demorar, verifique o link)")