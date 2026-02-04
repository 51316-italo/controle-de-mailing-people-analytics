# Schema da Base Final de Mailing – People Analytics

Este documento descreve o **schema da base final gerada pelo pipeline de limpeza em Python**.  
A base resultante é utilizada como **fonte única de verdade** para importação e análise no Power BI.

O schema é composto por:
- Campos originais (RAW)
- Campos tratados e padronizados (LIMPOS)
- Flags de descarte
- Metadados de controle e execução


## 🧾 1. Identificação e Dados Pessoais

| Coluna | Tipo | Descrição |
|------|------|-----------|
| Data Form | Data | Data de preenchimento do formulário |
| Nome | Texto | Nome informado originalmente |
| Nome Limpo | Texto | Nome padronizado após limpeza |
| CPF | Texto | CPF informado originalmente |
| CPF Limpo | Texto | CPF padronizado e validado |
| Idade | Número | Idade informada |
| Idade Limpo | Número | Idade validada após regras |
| Escolaridade | Texto | Escolaridade informada |
| Escolaridade Limpo | Texto | Escolaridade padronizada |

---

## 📞 2. Contato

| Coluna | Tipo | Descrição |
|------|------|-----------|
| Telefone | Texto | Telefone principal informado |
| Telefone 2 | Texto | Telefone secundário |
| Telefone Limpo | Texto | Telefone principal tratado |
| Telefone 2 Limpo | Texto | Telefone secundário tratado |
| Email | Texto | E-mail informado |
| Email Limpo | Texto | E-mail validado e padronizado |

---

## 🌍 3. Localização

| Coluna | Tipo | Descrição |
|------|------|-----------|
| Endereco | Texto | Endereço informado |
| Endereco Limpo | Texto | Endereço padronizado |
| Cidade de Origem | Texto | Cidade informada pelo lead |
| Cidade de Origem Limpo | Texto | Cidade de origem padronizada |
| Cidade da Vaga | Texto | Cidade da vaga |
| Cidade da Vaga Limpo | Texto | Cidade da vaga padronizada |
| Cidade | Texto | Cidade consolidada para análise |

---

## 🧑‍💼 4. Informações de Negócio / Recrutamento

| Coluna | Tipo | Descrição |
|------|------|-----------|
| Cargo | Texto | Cargo pretendido |
| Experiência Relevante | Texto | Informação sobre experiência |
| Modalidade da Entrevista | Texto | Modalidade da entrevista |
| Turno | Texto | Turno da vaga |
| Fonte | Texto | Fonte original do lead |
| Fonte Limpa | Texto | Fonte padronizada |
| Codigo Fonte | Texto | Código identificador da fonte |
| Fla
