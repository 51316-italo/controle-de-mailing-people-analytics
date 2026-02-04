# Schema da Base Final de Mailing – People Analytics

Este documento descreve o **schema da base final gerada pelo pipeline de limpeza em Python**.  
A base resultante é utilizada como **fonte única de verdade** para importação e análise no Power BI.

O schema é composto por:
- Campos originais (RAW)
- Campos tratados e padronizados (LIMPOS)
- Flags de descarte
- Metadados de controle e execução

---

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
| Flag Cvortex | Booleano | Indica origem via Cvortex |

---

## 🧾 5. Indicação

| Coluna | Tipo | Descrição |
|------|------|-----------|
| Matricula Indicador | Texto | Matrícula do indicador |
| Matricula Indicador Limpo | Texto | Matrícula do indicador tratada |
| Nome Indicador | Texto | Nome do indicador |
| Nome Indicador Limpo | Texto | Nome do indicador padronizado |

---

## ⏱️ 6. Datas e Metadados de Execução

| Coluna | Tipo | Descrição |
|------|------|-----------|
| Data Captacao | Data | Data de captação do lead |
| Datetime de Execução | Data/Hora | Momento da execução do pipeline |
| Data do Exame | Data | Data do exame admissional |
| Planilha | Texto | Nome da planilha de origem |

---

## 🔢 7. Controles e Contagens

| Coluna | Tipo | Descrição |
|------|------|-----------|
| Contagem CPF | Número | Quantidade de ocorrências do CPF |
| Contagem Telefone | Número | Quantidade de ocorrências do telefone |

---

## 🚫 8. Flags de Descarte

Estas colunas indicam se o lead deve ser descartado com base em regras de negócio.

| Coluna | Tipo | Descrição |
|------|------|-----------|
| Descarte Cidade | Booleano | Cidade fora do escopo |
| Descarte Telefone Invalido | Booleano | Telefone inválido |
| Descarte Contagem CPF | Booleano | CPF duplicado |
| Descarte Contagem Telefone | Booleano | Telefone duplicado |
| Descarte Idade | Booleano | Idade fora do permitido |
| Descarte Escolaridade | Booleano | Escolaridade incompatível |
| Descarte Atendimento Ativo | Booleano | Lead com atendimento ativo |
| Descarte Sucesso 30 Dias | Booleano | Sucesso recente (30 dias) |
| Descarte 7 Dias | Booleano | Reprocessamento em menos de 7 dias |

---

## 📌 Observações Gerais

- As colunas **RAW** são preservadas para rastreabilidade
- As colunas **LIMPAS** são utilizadas para análise e regras
- O Power BI consome prioritariamente os campos limpos
- As flags permitem análises detalhadas de descarte sem perda de histórico

Este schema pode evoluir conforme novas regras e fontes forem adicionadas ao pipeline.
