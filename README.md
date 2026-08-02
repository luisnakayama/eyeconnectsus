# EyeConnect SUS

Aplicação de triagem oftalmológica desenvolvida pelo **Núcleo de Saúde Digital (NSD)** da UNIFESP - **GAT 9** em parceria com o **Projeto de Extensão PET-Saúde**.

## 🔍 Sobre

EyeConnect SUS é um sistema de suporte à decisão clínica para triagem oftalmológica. A aplicação permite que profissionais de saúde realizem triagem de pacientes com queixas oftalmológicas, fornecendo recomendações de conduta baseadas em protocolos estabelecidos.

## ✨ Funcionalidades

- **Cadastro de Pacientes**: Registro de informações demográficas e de contato
- **Novo Atendimento**: Coleta estruturada de queixa principal, histórico oftalmológico e exame físico
- **Triagem Inteligente**: Análise das informações com recomendação de conduta
- **Histórico de Atendimentos**: Consulta de atendimentos anteriores
- **Teleconsulta**: Informações sobre modalidade de consulta remota
- **Protocolos**: Acesso aos protocolos clínicos utilizados
- **Especialistas**: Listagem de especialistas disponíveis
- **Notificações**: Sistema de alertas e mensagens
- **Perfil**: Gerenciamento de dados do usuário

## 🛠️ Tecnologias

- **Python 3.8+**
- **Streamlit** - Framework para web apps
- **Pandas** - Análise de dados

## 📋 Requisitos

```
streamlit>=1.28.0
pandas>=1.3.0
```

## 🚀 Como Executar

1. Clone o repositório:
```bash
git clone https://github.com/luisnakayama/eyeconnectsus.git
cd eyeconnectsus
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
streamlit run eyeconnect_app.py
```

A aplicação abrirá em `http://localhost:8501`

## 📱 Acessar Online

A aplicação está disponível em: [EyeConnect SUS](https://eyeconnectsus.streamlit.app)

## 👥 Autores

- **Núcleo de Saúde Digital (NSD)** - UNIFESP
- **PET-Saúde** - Projeto de Extensão

## 📄 Licença

Todos os direitos reservados © 2024 UNIFESP
