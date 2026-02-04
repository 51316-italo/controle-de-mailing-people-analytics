config = {
    # Caminho da pasta cujos mailings extraidos são disponibilizados para leitura (input):
    "input_path": "./Input",
    # Caminho da pasta onde o mailing compilado, arquivo com todas as informações da limpeza, será salvo (output):
    "output_path": "./Mailing Auto",
    # Caminho da pasta onde os arquivos de importação da central serão salvos, divididos por cidade e quebra de fonte (configuravel abaixo):
    "central_path": "./Central",
    # Caminho da pasta onde as imagens dos reports serão salvas (com relatorio de descartes de leads):
    "report_path": "./Report",
    # Cidades de atuação (para critérios de descarte - cidades não listadas são removidas):
    "cidades": ["uberlandia", "jundiai", "barueri", "aracaju", "hortolandia"],
    # Mapping de fontes (nomes padronizados e palavras chave para identificação):
    "fontes": {
        "INDEED": ["indeed"],
        "INDIQUE AMIGOS": ["indi"],
        "SENIOR": ["senior", "site"],
        "G.R.S": ["grs", "redessociais"],
        "CURRICULOS": ["curricu"],
        "GOOGLE ADS": ["rhcontratacao"],
        "GOOGLE EXT": ["google"],
        "LINKEDIN": ["linkedin"],
        "SALAS": ["sala"],
        "CAPTACAO EXTERNA": ["extern", "panflet"],
        "SINE": ["sine"],
        "VEREADORES": ["vereador"],
        "FACULDADES": ["ifp", "uniube", "anhanguera", "grautech"],
        "EVENTOS": ["event"],
        "LEADS SEMENTES": ["semente"],
        "ORGANICO GA": ["organico"],
        "TIKTOK": ["tiktok"],
        "FACEBOOK MD 50+": ["50"],
        "FACEBOOK MD": ["tardenoite", "aberto", "facebook", "meta", "instagram"],
        "BASE EXTRA": ['extra'],
    },
    # Critérios de quebra de planilhas (prioridade na ordem listada). Incluir fontes que deseja arquivos separados de importação:
    "quebra_fonte": [
        # "SALA",
        # "INDIQUE",
        #"INDEED"
    ],
    # Definição dos arquivos de entrada (input) e seus layouts (colunas):
    # Parametros possíveis:
    # `path`: Caminho do arquivo (dentro da pasta input_path)
    # `sheet`: Nome da planilha (se aplicável, no caso de excel)
    # `layout`: Nome do layout (definido abaixo)
    # `sep`: Separador do arquivo (se aplicável, no caso de csv)
    # `fonte_padrao`: Fonte padrão (quando deseja sobrescrever todo o arquivo com uma fonte)
    "sheets": {
        "indique_udia": {
            "path": "Indicou_ Contratou_ Ganhou!.xlsx",
            "sheet": "Mailing",
            "layout": "indique",
            "fonte_padrao": "INDIQUE UDIA"
        },
        "indique_sp": {
            "path": "INDIQUE AMIGO.xlsx",
            "sheet": "Mailing",
            "layout": "indique",
            "fonte_padrao": "INDIQUE SP"
        },
        "facaparte": {
            "path": "Faça parte da nossa equipe! 1.xlsx",
            "sheet": "Mailing",
            "layout": "facaparte"
        },
        "campanhas": {
            "path": "Acompanhamento de Mailing.xlsx",
            "sheet": "Acompanhamento de Mailing",
            "layout": "campanhas"
        },
        "indeedmt1": {
            "path": "CONFIDENCIAL_Atendente_de_Telemarketing_-_(_NÃO_É_NECESSÁRIO_EXPERIENCIA_)_candidatos.csv",
            "layout": "indeed",
            "sep": ",",
            "fonte_padrao": "INDEED UDIA M/T"
        },
        "indeedmt2": {
            "path": "CONFIDENCIAL_Atendente_de_Telemarketing_-_com_ou_sem_experiência_candidatos.csv",
            "layout": "indeed",
            "sep": ",",
            "fonte_padrao": "INDEED UDIA M/T"
        },
        "indeedmt3": {
            "path": "CONFIDENCIAL_Atendente_de_Operações_-com_ou_sem_experiência_candidatos.csv",
            "layout": "indeed",
            "sep": ",",
            "fonte_padrao": "INDEED UDIA M/T"
        },
        "indeedmt4": {
            "path": "CONFIDENCIAL_Atendente_de_Telemarketing_(_RECEPTIVOATIVO_)_+_GANHOS_EXTRAS_TARDENOITE_candidatos.csv",
            "layout": "indeed",
            "sep": ",",
            "fonte_padrao": "INDEED UDIA M/T"
        },
        "indeedtn1": {
            "path": "CONFIDENCIAL_ATENDENTE_DE_TELEMARKETING_-_TARDENOITE_(Não_é_necessário_experiência)_candidatos.csv",
            "layout": "indeed",
            "sep": ",",
            "fonte_padrao": "INDEED UDIA T/N"
        },
        "indeedtn2": {
            "path": "CONFIDENCIAL_Consultor(a)_de_Vendas_por_Teleatendimento_-_TardeNoite_candidatos.csv",
            "layout": "indeed",
            "sep": ",",
            "fonte_padrao": "INDEED UDIA T/N"
        },
        "indeedtn3": {
            "path": "CONFIDENCIAL_ATENDENTE_DE_TELEMARKETING_-_TARDENOITE_candidatos.csv",
            "layout": "indeed",
            "sep": ",",
            "fonte_padrao": "INDEED UDIA T/N"
        },
        "indeedtn4": {
            "path": "CONFIDENCIAL_Consultor(a)_de_Vendas_por_Teleatendimento_-_TardeNoite_candidatos.csv",
            "layout": "indeed",
            "sep": ",",
            "fonte_padrao": "INDEED UDIA T/N"
        },
        "tecnico_operacional_sp": {
            "path": "CONFIDENCIAL_Técnico_Operacional_Multicanal_candidatos.csv",
            "layout": "indeed",
            "sep": ",",
            "fonte_padrao": "INDEED SP"
        },
        "tecnico_operacional_sp2": {
            "path": "CONFIDENCIAL_Técnico_Operacional_candidatos.csv",
            "layout": "indeed",
            "sep": ",",
            "fonte_padrao": "INDEED SP"
        },
        "operador_atendimento_sp": {
            "path": "CONFIDENCIAL_Operador_de_Atendimento_-_Jundiaí_candidatos.csv",
            "layout": "indeed",
            "sep": ",",
            "fonte_padrao": "INDEED SP"
        },
         "analista_BKO_sp": {
            "path": "CONFIDENCIAL_Analista_Operacional_(_BackOffice_)_candidatos.csv",
            "layout": "indeed",
            "sep": ",",
            "fonte_padrao": "INDEED SP"
        },
        "tecnico_prevencao_fraude_sp": {
            "path": "CONFIDENCIAL_Técnico_de_Prevenção_a_Fraudes_candidatos.csv",
            "layout": "indeed",
            "sep": ",",
            "fonte_padrao": "INDEED SP"
        },
        "analista_operacional_sp": {
            "path": "CONFIDENCIAL_Analista_Operacional_candidatos.csv",
            "layout": "indeed",
            "sep": ",",
            "fonte_padrao": "INDEED SP"
        },
        "mailing": {
            "path": "MAILING.csv",
            "layout": "mailing",
            "sep": ";"
        },
    },
    # Definição dos layouts (colunas) de cada arquivo de entrada:
    #
    # Colunas essenciais de cada layput:
    # `Data Form` - Data do envio do formulário (para ordenação dos leads)
    # `Nome` - Nome do candidato
    # `CPF` - CPF do candidato
    # `Telefone` - Telefone principal do candidato
    # `Telefone 2` - Segundo telefone do candidato
    # `Cidade da Vaga` - Cidade onde a vaga está localizada
    # `Fonte` - Fonte de onde o lead foi extraído (se não houver, será necessario a fonte_padrao do arquivo)
    #
    # Colunas opcionais (incluir se disponível):
    # `Email` - E-mail do candidato
    # `Cidade de Origem` - Cidade onde o candidato reside
    # `Escolaridade` - Escolaridade do candidato
    # `Idade` - Idade ou data de nascimento do candidato (se aplicável)
    # `Matricula Indicador` - Matrícula do colaborador que indicou o candidato (se aplicável)
    # `Nome Indicador` - Nome do colaborador que indicou o candidato (se aplicável)
    # `Experiência Relevante` - Campo para experiência relevante do candidato (se aplicável)
    # `Cargo` - Cargo da vaga (se aplicável)
    "layouts": {
        "indeed": {
            "Nome": 0,
            "Email": 1,
            "Telefone": 2,
            "Cidade de Origem": 4,
            "Experiência Relevante": 5,
            "Escolaridade": 6,
            "Cargo": 7,
            "Cidade da Vaga": 8,
            "Data Form": 9
        },
        "facebook": {
            "Nome": "full name",
            "Escolaridade": "qual_o_seu_nível_de_escolaridade?",
            "CPF": "cpf",
            "Idade": "date_of_birth",
            "Cidade de Origem": "em_que_cidade_você_mora?",
            "Telefone": "informe_seu_whatsapp_para_entrarmos_em_contato.",
            "Telefone 2": "phone_number",
            "Email": "email",
            "Fonte": "adset_name",
            "Data Form": "created_time"
        },
        "facaparte": {
            "Data Form": "Hora de conclusão",
            "Nome": "QUAL O SEU NOME COMPLETO?",
            "CPF": "QUAL O SEU NÚMERO DE CPF (APENAS NÚMEROS)?",
            "Idade": "QUAL SUA DATA DE NASCIMENTO?",
            "Cidade da Vaga": "EM QUAL CIDADE VOCÊ GOSTARIA DE TRABALHAR CONOSCO?",
            "Escolaridade": "QUAL SUA ESCOLARIDADE?",
            "Telefone": "QUAL SEU TELEFONE DE CONTATO? (LIGAÇÃO E/OU WHATSAPP - APENAS NÚMEROS COM DDD):",
            "Telefone 2": "VOCÊ TEM OUTRO TELEFONE CASO NÃO ATENDA NO PRIMEIRO? INSIRA ABAIXO (APENAS NÚMEROS COM DDD):",
            "Fonte": "VOCÊ PODE NOS INDICAR QUAL O CANAL QUE TE TROUXE ATÉ NOSSA OPORTUNIDADE?"
        },
        "indique": {
            "Data Form": "Hora de conclusão",
            "Nome": "NOME DO AMIGO INDICADO",
            "CPF": "CPF DO AMIGO INDICADO",
            "Idade": "É MAIOR DE 18 ANOS?",
            "Escolaridade": "QUAL A ESCOLARIDADE DO AMIGO INDICADO? ",
            "Cidade da Vaga": "EM QUAL CIDADE SEU AMIGO QUER TRABALHAR?",
            "Telefone": "TELEFONE DO AMIGO INDICADO (COM WHATSAPP):",
            "Telefone 2": "SEGUNDO TELEFONE (SE HOUVER):",
            "Matricula Indicador": "QUAL A SUA MATRÍCULA / ENUMBER? (APENAS NÚMEROS)",
            "Nome Indicador": "NOME COMPLETO DO COLABORADOR? (QUEM ESTÁ INDICANDO)"
        },
        "campanhas": {
            "Data Form": "Data de Criação",
            "Nome": "Nome Lead",
            "Idade": "Data de Nascimento",
            "CPF": "CPF",
            "Escolaridade": "Formação",
            "Telefone": "Auxiliar 07",
            "Telefone 2": "Auxiliar 08",
            "Cidade da Vaga": "Cidade",
            "Fonte": "Plataforma de origem"
        },
        "mailing": {
            "Data Form": "DATA",
            "Nome": "NOME",
            "CPF": "CPF",
            "Telefone": "TELEFONE",
            "Telefone 2": "TELEFONE 2",
            "Fonte": "FONTE",
            "Cidade da Vaga": "REGIÃO"
        },
    }
}
