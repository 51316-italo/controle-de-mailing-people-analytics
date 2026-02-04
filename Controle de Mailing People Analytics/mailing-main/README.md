# Módulo de Automação do Mailing

Este módulo automatiza o processo de coleta e limpeza de leads no mailing, passando pelo BIGO e Visual Studio de seleção, até a separação de arquivos para envio à Central, gerando uma base pronta para importação no Power BI.

# Download e Configuração

Para utilizar este módulo, devem ser realizados os seguintes passos de configuração. Esta etapa precisa ser seguida apenas uma vez, no primeiro uso, para preparar o ambiente corretamente.

## 1. Instalar o Python na máquina

Se você já tiver o Python instalado, pode pular este passo. Caso contrário, basta acessar o portal Antares
 do Service Desk e, em Solicitações, realizar a instalação do Python em sua máquina.

## 2. Baixar este repositório

Este repositório está localizado no GitHub
.
Ao acessá-lo, é necessário clicar em <> Code, no canto superior direito, onde você encontrará a opção Download ZIP, que permitirá baixar uma pasta compactada. Após extraí-la, você terá todo o ferramental necessário para utilizar este módulo.

## 3. Rodar o arquivo de configuração

Ao configurar o ambiente pela primeira vez, é necessário instalar algumas dependências no Python. Para isso, existe o executável config na pasta principal. Se a execução ocorrer sem erros, seu ambiente estará pronto para rodar a aplicação.

# Módulo de Limpeza

Este módulo tem como objetivo gerar, com base no mailing bruto extraído, os arquivos CSV para importação de contatos pela Central, além das imagens de relatório da limpeza do mailing diário.

# Requisitos

Para utilizar este módulo, é necessário extrair todas as fontes de mailing disponíveis e colocar os arquivos na pasta de entrada, que pode ser configurada em src/config.json.

# Execução

Para rodar este módulo, basta abrir o arquivo run. Ao executá-lo, você será solicitado a informar alguns dados para a geração das planilhas, sendo eles, em ordem:

## Módulo a executar: 
Insira o número 1 para a limpeza.

## Modo de debug: 
Insira v para rodar em modo de debug. Para o modo normal, basta pressionar Enter.

## Prefixo dos arquivos: 
Por padrão, o prefixo no nome dos arquivos é o turno de execução (basta pressionar Enter). Caso queira, é possível definir outro prefixo para execuções separadas. Cada prefixo gera um registro. Caso execute com um prefixo já existente, será questionado se deseja sobrescrever a última execução, podendo seguir em frente ou cancelar o processo.

## Salvamento no banco de dados: 
Após algumas etapas de processamento, será perguntado se deseja salvar o histórico no banco de dados de People Analytics (atualmente este processo está apenas em planejamento, pois a área de People Analytics não dispõe de um servidor próprio para criação de um banco de dados).

## Definição da quantidade de arquivos gerados para importação: 
Como etapa final, é exibido um script solicitando a entrada do usuário com a quantidade de arquivos para importação que deseja gerar por cidade, conforme configurado em config.py.

Pronto. Com a execução ocorrendo normalmente, os arquivos finais serão gerados nas respectivas pastas.
