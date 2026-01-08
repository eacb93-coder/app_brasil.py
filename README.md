# 🚗 Gestor de Locadora Brasil (Intelligent Upsell System)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![Data](https://img.shields.io/badge/Data-Google%20Sheets%20%2F%20Pandas-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

> **Uma solução de automação comercial que integra dados em nuvem (Google Sheets) com lógica de vendas algorítmica para maximizar o ticket médio de locadoras de veículos.**

---

## 🎯 O Problema de Negócio
Locadoras de veículos perdem receita diariamente devido a dois fatores:
1.  **Falha de Comunicação:** Demora para atualizar preços e disponibilidade entre a gestão de frota (Planilha) e o time de vendas.
2.  **Oportunidades Perdidas:** Atendentes que não aplicam técnicas de *Upsell* (oferta de categoria superior) de forma consistente em períodos de alta demanda.

## 💡 A Solução Técnica
Desenvolvi uma aplicação web em **Python (Streamlit)** que atua como uma interface centralizada e inteligente:

* **Integração Cloud em Tempo Real:** O sistema consome dados diretamente de um **Google Sheets** via API pública (CSV), eliminando versões desatualizadas de arquivos locais.
* **Algoritmo de "Isca" & Upsell:** O código detecta automaticamente quando um cliente solicita um "Carro Isca" (preço promocional/esgotado) e gera instantaneamente um script de vendas persuasivo focado em converter para categorias superiores (SUV/Turbo).
* **Inteligência Sazonal:** A lógica do sistema ajusta os argumentos de venda baseando-se na data da reserva (ex: *Reveillon* foca em escassez; *Férias* foca em conforto).

---

## 📸 Hero Shot (Interface do Sistema)

![Screenshot do Sistema](https://seulinkdaimagem.com/print.png)

*O sistema detectando um cenário de Alta Temporada e sugerindo upgrades automaticamente.*

---

## 🛠️ Stack Tecnológico

* **Linguagem:** Python 3.12
* **Front-end:** Streamlit (para renderização rápida de dashboards).
* **Manipulação de Dados:** Pandas (ETL e limpeza de dados).
* **Conectividade:** Integração via URL CSV do Google Sheets.
* **Arquitetura:** Lógica separada em camadas (Data fetching, Business Logic, UI).

---

## 🚀 Como Executar Localmente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/gestor-locadora-brasil.git](https://github.com/SEU-USUARIO/gestor-locadora-brasil.git)
    cd gestor-locadora-brasil
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a aplicação:**
    ```bash
    streamlit run app_brasil.py
    ```

---

## 🧠 Destaques de Código (Programação Defensiva)

O sistema foi construído com foco em robustez para evitar falhas em produção:

* **Tratamento de Erros de Conexão:** O sistema não "crasha" se a internet cair; ele exibe mensagens de erro amigáveis ao usuário.
* **Sanitização de Dados:** O Pandas remove linhas vazias ou corrompidas vindas do Google Sheets antes do processamento.
* **Cache Inteligente (`@st.cache_data`):** Implementação de cache para reduzir o consumo de dados e latência, melhorando a experiência do usuário.

---

## 👤 Sobre o Autor

Desenvolvedor com background em Administração e Auditoria, focado em criar ferramentas que transformam processos manuais em automação estratégica.

linkedin.com/in/eloirborges/
