<p style="text-align:center;">RH Callink</p>

_____
# Módulo de Automação do Mailing

Este módulo automatiza o processo de coleta e limpeza de leads no mailng, passando pelo BIGO e Visual Studio de seleção, até a separação de arquivos para o envio para a Central e gerando uma base pronta para importação no PBI.

## Download e Configuração

Para utlizar esse módulo, deve-se realizar os seguintes passos de configuração. Esta etapa só precisa ser seguida uma vez, no primeiro uso, para configurar seu ambiente para utilização.

### 1. Instalar o Python na Máquina

Se você já tiver o python instalado, pode pular essse passo. Caso contrário, basta acessar o portal [Antares](https://antares.callink.com.br/) do Service Desk e, em solicitações, instalar o Python em sua máquina.

### 2. Baixar esse repositório

Esse repositório está localizado no [GitHub](https://github.com/51316-italo/controle-de-mailing-people-analytics/tree/main). Ao acessá-lo, é preciso clicar em `<>Code` no canto superior direito, onde você encontrará `Download ZIP`, que permitira baixar uma pasta compactada que, após extraída, teá todo o ferramental necessário para utilizar esse módulo.

### 3. Rodar o arquivo de configuração

Quando configurando o ambiente pela primeira vez, é preciso instalar algumas dependências no seu python. Para isso, existe o exectável `config` na pasta principal. Se a execussão ocorrer sem erros, seu ambiente estará pronto para rodar o app.


## Módulo Limpeza

Este módulo visa gerar, com base no mailing bruto extraído, os arquvos CSV para importação de contato pela Central e as imagens de relatório da limpeza do mailing diário.

### Requisitos

Para utulizar esse módulo, é preciso extrair todas as fontes de mailing siponíveis e colocar os arquivos na pasta de entrada, que pode ser editada em `src/config.json`.

### Execussão

Para rodar este módulo, basta abrir o arquivo `run`. Ao abrir, você será solicitado a responder algumas informações para a geração das planilhas, sendo elas, em ordem:

- **Módulo a executar:** Insira o número `1` para a limpeza.
- **Modo de Debug:** Inserir `v` para rodar em modo de debug. Para o modo normal, bata pressionar `Enter`.
- **Prefixo dos arquivos:** Por padrão, o prefixo no nome dos arquivos é o turno de execução (basta apertar ENTER). Caso queira, pode definir outro prefixo para execuções separadas. Cada prefixo gera um registro. Caso execute com outro prefixo será queistonado se deseja sobrescrever a ultima execução, e poderá seguir em frente ou cancelar o processo.
- **Salvamento no banco de Dados:** Depois de algumas etapas de processamento, sera perguntado se deseja savar o historico no Banco de Dados de People Analytics (atualmente esse processo está apenas em planejamento pois como a área de People Analytics não dispõe de um server proóprio não é possivél criar um DB).
- **Definição da quantidade de arquivos gerados para importação** Como etapa final é exibido um scripet solicitando a entrada do usuário da quantidade de arquivos para importação que o mesmo deseja gerar por cidade que conta nas bases de entrada e salvas em config.py

Pronto, a execussão ocorrendo normalmente os arquivos finais serão gerados nas devidas pastas. 
