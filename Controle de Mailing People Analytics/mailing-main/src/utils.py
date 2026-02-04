import pandas as pd
import unicodedata
import requests
import logging
import json
import re
import os

from datetime import datetime, timedelta
from sqlalchemy import create_engine
from typing import Dict, Any, Callable, Optional
import matplotlib.pyplot as plt
from tabulate import tabulate
from typing import Optional, Union
from config import config


def print_logo():
    logo = """
    ██████╗ ███████╗ ██████╗ ██████╗ ██╗     ███████╗         █████╗ ███╗   ██╗ █████╗ ██╗   ██╗   ██╗█████████╗██╗ ██████╗███████╗
    ██╔══██╗██╔════╝██╔═══██║██╔══██╗██║     ██╔════╝        ██╔══██╗████╗  ██║██╔══██╗██║   ╚██╗ ██╔╝╚══██╔══╝ ██║██╔════╝██╔════╝
    ██████╔╝█████╗  ██║   ██║██████╔╝██║     █████╗          ███████║██╔██╗ ██║███████║██║    ╚████╔╝    ██║    ██║██║     ███████╗
    ██╔═══╝ ██╔══╝  ██║   ██║██╔═══╝ ██║     ██╔══╝          ██╔══██║██║╚██╗██║██╔══██║██║     ╚██╔╝     ██║    ██║██║     ╚════██║
    ██║     ███████╗╚██████╔╝██║     ███████╗███████╗        ██║  ██║██║ ╚████║██║  ██║███████╗ ██║      ██║    ██║╚██████╗███████║
    ╚═╝     ╚══════╝ ╚═════╝ ╚═╝     ╚══════╝╚══════╝        ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝ ╚═╝      ╚═╝    ╚═╝ ╚═════╝╚══════╝
    """
    print(logo)


def config_logger(verbose):
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(
                f'logs/limpeza_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'
            ),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(__name__)


def get_user_input(prompt, valid_inputs=None, default=False, return_raw=False):
    """
    Lida com a entrada do usuário com validação.
    Args:
        prompt (str): O texto a ser exibido para o usuário.
        valid_inputs (list, opcional): Lista de entradas válidas. Padrão é None.
        default (bool): Valor padrão se nenhuma entrada for fornecida. Padrão é False.
        return_raw (bool): Se True, retorna a entrada original do usuário em vez de um booleano. Padrão é False.
    Returns:
        bool ou str: True se a entrada corresponder às entradas válidas, caso contrário False.
                    Se return_raw for True, retorna a entrada original do usuário.
    """
    if return_raw:
        while True:
            x = input(prompt)
            if not pd.isna(x):
                x = clean_text(x).lower()
                if x in valid_inputs:
                    return x
            print(f"Entrada inválida. Por favor, tente novamente.")
    if valid_inputs:
        x = input(prompt)
        return x.lower() in valid_inputs
    return default


def get_run_params():
    """
    Obtém os parâmetros de execução do usuário.
    Returns:
        verbose (bool): Indica se o modo de debug está ativado.
    """
    verbose = get_user_input(
        "Pressione Enter para executar normalmente ou digite 'v' para modo de debug: ",
        valid_inputs=["v", "verbose"])
    return verbose


def get_grupo_prefixo(logger, out_path):
    """
    Define o turno e o prefixo dos arquivos de saída com base no horário atual e entrada do usuário.
    Caso o arquivo com o prefixo gerado já exista no diretório de saída, o usuário será questionado se deseja sobrescrevê-lo.
    Se o usuário optar por não sobrescrever, a função será chamada recursivamente para redefinir o turno e o prefixo.
    Args:
        logger (logging.Logger): Instância do logger para registrar mensagens de log.
        out_path (str): Caminho do diretório onde os arquivos serão salvos.
    Returns:
        tuple: Uma tupla contendo:
            - turno (str): O turno definido pelo usuário ou padrão baseado no horário atual ('manha', 'tarde', 'noite').
            - prefixo (str): Prefixo formatado para os arquivos de saída, incluindo a data e o turno.
    """
    current_time = datetime.now().time()
    if current_time < datetime.strptime("11:00", "%H:%M").time():
        turno = 'manha'
    elif current_time < datetime.strptime("14:00", "%H:%M").time():
        turno = 'tarde'
    else:
        turno = 'noite'
    grupo = input(
        f"Defina o prefixo dos arquivos (Aperte ENTER para padrão: '{turno}'): ")
    grupo = turno if not grupo else clean_text(grupo)
    prefixo = f"/{datetime.now().strftime("%Y_%m_%d")}_{grupo}_"
    logger.debug(f"Turno: {turno} | Grupo: {grupo} | Prefixo: {prefixo}")
    logger.debug(
        f"Verificando existência do arquivo {out_path + prefixo + 'Mailing.xlsx'}")
    if os.path.exists(out_path + prefixo + "Mailing.xlsx"):
        overwrite = get_user_input(
            f"AVISO! O arquivo com prefixo '{prefixo[1:-1]}' já existe, deseja mesmo substitui-lo? Se sim, insira 'sim'/'s'/'yes'/'y' (Enter para alterar): ", ['sim', 's', 'yes', 'y'])
        logger.debug(f"Overwrite definido para {overwrite}")
        if not overwrite:
            return get_grupo_prefixo(logger, out_path)
    return grupo, prefixo


def determine_planilha(linha, quebra_fonte):
    """
    Determina o nome da planilha com base nas informações normalizadas de cidade e fonte.
    Args:
        linha (dict): Uma linha de um dataframe contendo as chaves 'Cidade_Normalizada' e 'Fonte_Normalizada'.
        quebra_fonte (list): Uma lista de substrings para comparar com a fonte normalizada (definido nas configurações).
    Returns:
        str: Uma string representando o nome da planilha no formato "{planilha}_{cidade}".
             O `planilha` é determinado ao comparar substrings em `quebra_fonte` com a fonte 
             normalizada, e `cidade` é definido como "URA" ou "UDIA" com base na cidade normalizada.
    """
    cidade = linha['Cidade_Normalizada'].upper()
    fonte = linha['Fonte_Normalizada']
    planilha = 'DEMAIS'
    for subfonte in quebra_fonte:
        if subfonte.lower() in fonte:
            planilha = subfonte
    return f"{planilha}_{cidade}"


def decide_planilha(logger, df, quebra_fonte, fonte_col='Fonte Limpa'):
    """
    Define a coluna "Planilha" no DataFrame com base em regras específicas.
    Args:
        logger (logging.Logger): Logger para registrar informações e depuração.
        df (pd.DataFrame): DataFrame contendo os dados.
        sala_aberta (Optional[bool]): Indica se o evento Sala Aberta está ativo.
        fonte_col (str): Nome da coluna que contém as fontes. Padrão é "Fonte".
    Returns:
        pd.DataFrame: DataFrame atualizado com a coluna "Planilha".
    """
    logger.debug("Iniciando a definição da coluna 'Planilha'.")
    # Normalizar as colunas para comparação
    df["Cidade_Normalizada"] = df["Cidade"].apply(
        lambda x: clean_text(x) if isinstance(x, str) else "")
    df["Fonte_Normalizada"] = df[fonte_col].apply(
        lambda x: clean_text(x) if isinstance(x, str) else "")
    df["Planilha"] = df.apply(
        lambda x: determine_planilha(x, quebra_fonte), axis=1)
    # Remover colunas normalizadas auxiliares
    df.drop(columns=["Cidade_Normalizada", "Fonte_Normalizada"], inplace=True)
    logger.debug("Coluna 'Planilha' definida com sucesso.")
    return df


def get_all_sheets(logger, folder, sheets, layouts):
    """
    Lê todas as abas especificadas no JSON, renomeia as colunas de acordo com o layout
    e combina os dados em um único DataFrame. O tipo do arquivo é determinado pelo final do nome do arquivo.
    Args:
        logger: Instância do logger para registrar logs.
        sheets (dict): Informações sobre as planilhas e abas a serem lidas.
        layouts (dict): Mapeamento de layouts para renomear colunas.
    Returns:
        pd.DataFrame: DataFrame combinado contendo os dados de todas as abas especificadas.
    """
    combined_df = pd.DataFrame()
    for sheet_name, sheet_info in sheets.items():
        path = folder + '/' + sheet_info.get("path")
        logger.debug(f"Path definido para {path}")
        aba = sheet_info.get("sheet")  # Apenas relevante para Excel
        layout_name = sheet_info.get("layout")
        # Valor padrão para a coluna "Fonte"
        fonte_padrao = sheet_info.get("fonte_padrao")
        layout = layouts.get(layout_name)
        if not path or not layout_name:
            logger.warning(
                f"Informações incompletas para a aba {sheet_name}. Pulando...")
            continue
        if not layout:
            logger.warning(
                f"Layout {layout_name} não encontrado. Pulando aba {sheet_name}...")
            continue
        # Determinar o tipo do arquivo pelo final do nome do arquivo
        if path.endswith(".xlsx") or path.endswith(".xls"):
            file_type = "excel"
        elif path.endswith(".csv"):
            file_type = "csv"
        else:
            logger.warning(
                f"Tipo de arquivo não suportado para {path}. Pulando {sheet_name}...")
            continue
        logger.debug(
            f"Lendo o arquivo {path} do tipo {file_type} com layout {layout_name}")
        try:
            if file_type == "excel":
                if not aba:
                    logger.warning(
                        f"Aba não especificada para o arquivo Excel {path}. Pulando...")
                    continue
                engine = "openpyxl" if path.endswith(".xlsx") else "xlrd"
                df = pd.read_excel(path, sheet_name=aba, engine=engine)
            elif file_type == "csv":
                header = None if 'CONFIDENCIAL' in path else 'infer'
                df = pd.read_csv(path, encoding="utf-8",
                                 header=header, sep=sheet_info.get('sep'))
                if not header:
                    df = df.iloc[1:]
            else:
                logger.warning(
                    f"Tipo de arquivo {file_type} não suportado. Pulando {sheet_name}...")
                continue
            logger.info(
                f"LEITURA REALIZADA - '{sheet_name}': {df.shape[0]} LEADS")
            logger.debug(
                f"LEITURA REALIZADA: Arquivo '{sheet_name}' em '{path}': {df.shape[0]} linhas e {df.shape[1]} colunas")
            # Renomear colunas e filtrar
            df = df[layout.values()]
            df = df.rename(columns={v: k for k, v in layout.items()})
            # Definir a coluna "Fonte" com o valor padrão, se especificado
            if fonte_padrao:
                logger.debug(
                    f"Definindo a coluna 'Fonte' com o valor padrão '{fonte_padrao}' para a aba {sheet_name}")
                df["Fonte"] = fonte_padrao
            # Adicionar dados ao DataFrame combinado
            if (len(df) > 0) & (len(combined_df) > 0):
                combined_df = pd.concat([combined_df, df], ignore_index=True)
            elif len(df) > 0:
                combined_df = df
            logger.debug(
                f"Dados do arquivo {path} processados e adicionados ao DataFrame combinado")
        except FileNotFoundError:
            logger.debug(
                f"LEITURA NÃO REALIZADA: Arquivo '{sheet_name}' em  '{path}' não encontrado")
        except KeyError as e:
            logger.error(f"Erro ao processar colunas do arquivo {path}: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao processar o arquivo {path}: {e}")
    logger.debug(
        f"Processamento concluído. DataFrame final contém {combined_df.shape[0]} linhas e {combined_df.shape[1]} colunas")
    return combined_df


def overwrite_excel(logger, df, output_file, sheet_name='Mailing'):
    """
    Sobrescreve uma aba existente em um arquivo Excel com um novo DataFrame.
    Caso ocorra um erro, solicita ao usuário que feche o arquivo e tente novamente.
    Args:
        logger (logging.Logger): Logger para registrar informações.
        df (pd.DataFrame): DataFrame a ser salvo.
        output_file (str): Caminho do arquivo Excel de saída.
        sheet_name (str): Nome da aba a ser sobrescrita.
    """
    while True:
        try:
            logger.debug(f"Escrevendo o DataFrame no arquivo {output_file}")
            with pd.ExcelWriter(output_file, engine="openpyxl", mode="w") as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            logger.debug(f"DataFrame salvo com sucesso na aba {sheet_name}")
            break
        except PermissionError:
            logger.error(
                f"Falha ao salvar o arquivo {output_file}. Verifique se o arquivo está aberto e feche-o.")
            input("Erro: Não foi possível salvar o arquivo. Certifique-se de que o arquivo está fechado e pressione ENTER para tentar novamente.")


def normalize_text(stylized_text):
    # Normaliza o texto para a forma NFKD
    normalized_text = unicodedata.normalize('NFKD', stylized_text)
    # Remove caracteres combinantes
    text_without_combining = ''.join(
        [c for c in normalized_text if not unicodedata.combining(c)])
    # Remove caracteres não alfanuméricos
    text_alphanumeric_only = ''.join(
        [c for c in text_without_combining if c.isalnum() or c == ' '])
    text_unique_spaces = re.sub(r'\s+', ' ', text_alphanumeric_only).strip()
    if max([len(x) for x in text_unique_spaces.split(' ')]) <= 1:
        return text_unique_spaces.replace(' ', '')
    return text_unique_spaces


def filter_numbers(text: Optional[str]) -> str:
    """
    Remove caracteres não numéricos de um texto.
    Args:
        text (str): O texto a ser processado.
    Returns:
        str: O texto contendo apenas números.
    """
    if pd.isna(text):
        return ""
    return re.sub(r"\D", "", str(text))


def calculate_cpf_digit(cpf: str, weight: int) -> int:
    """
    Calcula um dígito verificador de CPF.
    Args:
        cpf (str): O CPF em formato de string.
        weight (int): O peso inicial para o cálculo.
    Returns:
        int: O dígito verificador calculado.
    """
    total = sum(int(cpf[i]) * (weight - i) for i in range(len(cpf)))
    return (total * 10 % 11) % 10


def valida_cpf(logger, cpf: str) -> Optional[str]:
    """
    Valida um número de CPF.
    Args:
        cpf (str): O CPF em formato de string.
    Returns:
        Optional[str]: O CPF válido ou None se for inválido.
    """
    cpf = format_cpf(cpf)
    if pd.isna(cpf):
        return None
    if len(cpf) != 11 or cpf in ["00000000000", "99999999999"]:
        return None
    digit1 = calculate_cpf_digit(cpf[:9], 10)
    digit2 = calculate_cpf_digit(cpf[:10], 11)
    return cpf if cpf[-2:] == f"{digit1}{digit2}" else None


def camel_case(text: str) -> str:
    """
    Converte um texto para o formato Camel Case.
    Args:
        text (str): O texto a ser convertido.
    Returns:
        str: O texto em formato Camel Case.
    """
    return " ".join([w.capitalize() for w in text.split(" ")])


def limpa_nome(logger, nome: Optional[str]) -> Optional[str]:
    """
    Limpa e formata um nome, removendo caracteres especiais e acentuação.
    Args:
        nome (str): O nome a ser limpo.
    Returns:
        Optional[str]: O nome limpo ou None se o nome estiver vazio.
    """
    if pd.isna(nome) or nome == "" or not isinstance(nome, str):
        return None
    clean_name = camel_case(normalize_text(nome))
    return None if clean_name == "" else clean_name


def clean_text(text):
    """
    Remove espaços, pontuação e acentuação de um texto.
    Args:
        text (str): O texto a ser processado.
    Returns:
        str: O texto limpo.
    """
    # Remover espaços
    text = re.sub(r"\s+", "", str(text).lower())
    # Remover pontuação e acentuação
    text = normalize_text(text)
    return text


def valida_email(logger, email: Optional[str]) -> Optional[str]:
    """
    Valida se a string fornecida é um Endereco de e-mail válido.
    Args:
        email (Optional[str]): A string a ser validada como e-mail ou None.
    Returns:
        Optional[str]: O e-mail se for válido, caso contrário, None.
    """
    if pd.isna(email) or email == "":
        return None
    # Expressão regular para validar um e-mail
    email = email.replace(' ', '')
    regex_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(regex_email, email):
        return email.replace(' ', '')
    else:
        return None


def valida_idade(logger, idade: Union[str, int, datetime, None]) -> Optional[int]:
    """
    Valida e converte diferentes formatos de entrada para a coluna idade em anos.
    Args:
        idade (Union[str, int, datetime, None]): O elemento da coluna idade.
    Returns:
        Optional[int]: A idade em anos ou None se não for possível determinar a idade.
    """
    if pd.isna(idade) or idade == "":
        return None
    if isinstance(idade, int):
        return idade if idade <= 120 else None
    if isinstance(idade, datetime):
        return datetime.now().year - idade.year
    if isinstance(idade, str):
        idade = normalize_text(idade).lower()
        if idade == "sim":
            return "+18"
        if idade == "nao":
            return "<18"
        idade = filter_numbers(idade)
        # Verifica se a string tem até 3 dígitos
        if idade.isdigit() and len(idade) <= 3:
            return int(idade) if int(idade) <= 120 else None
        if idade.isdigit() and len(idade) == 4:
            return datetime.now().year - int(idade)
        # Tenta converter para data de nascimento no formato DDMMYYYY ou DDMMYY
        try:
            if len(idade) == 8:
                data_nascimento = datetime.strptime(idade, "%d%m%Y")
            elif len(idade) == 6:
                data_nascimento = datetime.strptime(idade, "%d%m%y")
            else:
                logger.debug(f"Falha ao converter idade: {idade}")
                return None
            return datetime.now().year - data_nascimento.year
        except ValueError:
            logger.debug(f"Falha ao converter idade: {idade}")
            return None
    return None


def limpa_escolaridade(logger, escolaridade: Optional[str]) -> Optional[str]:
    """
    Limpa e padroniza a escolaridade.
    Args:
        escolaridade (Optional[str]): A escolaridade a ser padronizada.
    Returns:
        Optional[str]: A escolaridade padronizada ou None se não for possível determinar a escolaridade.
    """
    if pd.isna(escolaridade) or escolaridade == "":
        return None
    escolaridade = clean_text(escolaridade)
    if 'posgraduacao' in escolaridade:
        return "Pos-Graduação"
    elif 'mestrado' in escolaridade:
        return "Mestrado"
    elif 'doutorado' in escolaridade:
        return "Doutorado"
    elif "superior" in escolaridade or "tecnico" in escolaridade or 'graduacao' in escolaridade:
        if "incompleto" in escolaridade:
            return "Superior Incompleto"
        else:
            return "Superior Completo"
    elif "medio" in escolaridade:
        if "incompleto" in escolaridade:
            return "Ensino Médio Incompleto"
        else:
            return "Ensino Médio Completo"
    elif "fundamental" in escolaridade:
        if "incompleto" in escolaridade:
            return "Fundamental Incompleto"
        else:
            return "Fundamental Completo"
    else:
        return None


def map_fonte(logger, df, fonte_col, fontes):
    """
    Mapeia os valores de uma coluna do DataFrame com base em um dicionário de fontes.
    Args:
        logger (logging.Logger): Logger para registrar informações e depuração.
        df (pd.DataFrame): DataFrame contendo os dados.
        fonte_col (str): Nome da coluna do DataFrame que será mapeada.
        fontes (dict): Dicionário onde as chaves são os valores mapeados e os valores são listas de substrings.
    Returns:
        pd.DataFrame: DataFrame atualizado com uma nova coluna 'Fonte Limpa' contendo os valores mapeados.
    """
    def mapear_fonte(valor):
        if pd.isna(valor) or valor.strip() == "":
            return ""
        valor_limpo = clean_text(valor)
        for chave, substrings in fontes.items():
            if any(substring in valor_limpo for substring in substrings):
                return chave
        logger.warning(f"Fonte não mapeada: '{valor}'")
        return ""
    logger.debug(f"Aplicando o mapeamento à coluna '{fonte_col}'.")
    df["Fonte Limpa"] = df[fonte_col].apply(mapear_fonte)
    logger.debug("Mapeamento concluído com sucesso.")
    return df


def padronizar_endereco(logger, endereco: Optional[str]) -> Optional[str]:
    """
    Padroniza um Endereco usando a API Nominatim do OpenStreetMap.
    Args:
        endereco (Optional[str]): A string do Endereco a ser padronizado.
    Returns:
        Optional[dict]: Um dicionário com o Endereco padronizado ou None se a entrada for None ou inválida.
    """
    if pd.isna(endereco) or endereco == "":
        return None
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": endereco,
        "format": "json",
        "addressdetails": 1,
        "limit": 1
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; MyApp/1.0)"
    }
    try:
        response = requests.get(
            url, params=params, headers=headers, verify=False)
        if response.status_code == 200:
            result = response.json()
            if result:
                return result[0].get("display_name", None)
            else:
                return None
        else:
            logger.debug(f"Erro na solicitação: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.debug(f"Erro na solicitação: {e}")
        return None


def limpar_telefone(logger, telefone: Optional[str]) -> Optional[str]:
    """
    Limpa e padroniza um número de telefone.
    Args:
        telefone (Optional[str]): O número de telefone a ser padronizado.
    Returns:
        Optional[str]: O número de telefone padronizado ou None se não for possível determinar o telefone.
    """
    if pd.isna(telefone) or telefone == "":
        return None
    elif isinstance(telefone, float):
        telefone = str(int(telefone))
    else:
        telefone = filter_numbers(telefone).lstrip('0')
    if len(telefone) < 8 or len(telefone) > 13:
        return None
    if len(telefone) == 8:
        if int(telefone[0]) < 6:
            return "34" + telefone
        return "349" + telefone
    if len(telefone) == 9:
        return "34" + telefone
    if len(telefone) == 10:
        if telefone.startswith("55"):
            if int(telefone[2]) < 6:
                return "34" + telefone[2:]
            return "349" + telefone[2:]
        if int(telefone[2]) < 6:
            return telefone
        return telefone[:2] + "9" + telefone[2:]
    if len(telefone) == 11:
        if telefone.startswith("55"):
            return "34" + telefone[2:]
        return telefone
    if len(telefone) == 12 and telefone.startswith("55"):
        if int(telefone[4]) < 6:
            return telefone[2:]
        return telefone[2:4] + "9" + telefone[4:]
    if len(telefone) == 13 and telefone.startswith("55"):
        return telefone[2:]
    return None


def limpa_matricula(logger, matricula: Optional[str]) -> Optional[str]:
    """
    Limpa e padroniza um número de matrícula.
    Args:
        matricula (Optional[str]): O número de matrícula a ser padronizado.
    Returns:
        Optional[str]: O número de matrícula padronizado ou None se não for possível determinar a matrícula.
    """
    if pd.isna(matricula):
        return None
    matricula = filter_numbers(matricula)
    if matricula == "":
        return None
    matricula = int(matricula)
    return f"{matricula}" if matricula > 0 else None


def add_date_column(logger, df, column_name="Data"):
    """
    Adiciona uma coluna com a data atual ao DataFrame fornecido.
    Args:
        df (pd.DataFrame): O DataFrame ao qual a coluna será adicionada.
        column_name (str): O nome da coluna de data. Padrão é "Data".
    Returns:
        pd.DataFrame: O DataFrame atualizado com a nova coluna de data.
    """
    today_date = datetime.now().strftime("%d/%m/%Y")
    # today_date = "04/05/2025"
    logger.debug(
        f"Adicionando coluna de data '{column_name}' com valor '{today_date}'")
    df[column_name] = today_date
    return df


def add_runtime_column(logger, df, column_name="Datetime de Execução"):
    """
    Adiciona uma coluna com a data e hora de execução ao DataFrame fornecido.
    Args:
        df (pd.DataFrame): O DataFrame ao qual a coluna será adicionada.
        column_name (str): O nome da coluna de data e hora. Padrão é "Datetime de Execução".
    Returns:
        pd.DataFrame: O DataFrame atualizado com a nova coluna de data e hora.
    """
    runtime = datetime.now().strftime("%Y-%m-%d")
    logger.debug(
        f"Adicionando coluna de data e hora '{column_name}' com valor '{runtime}'")
    df[column_name] = runtime
    return df


def combina_cidade(logger, df, col_list):
    """
    Combina os valores de várias colunas em uma única coluna de cidade.
    Args:
        logger: Instância do logger para registrar logs.
        df (pd.DataFrame): DataFrame contendo os dados.
        col_list (list): Lista de colunas a serem combinadas.
    Returns:
        pd.DataFrame: DataFrame atualizado com a nova coluna de cidade.
    """
    logger.debug(f"Combinando colunas {col_list} em uma única coluna")
    df["Cidade"] = df[col_list].apply(
        lambda row: next((x for x in row if pd.notnull(x)), None), axis=1).fillna('Uberlandia')
    return df


def filtra_idade(logger, idade):
    """
    Marca no DataFrame qualquer pessoa cuja idade seja menor que 18 anos.
    Args:
        logger: Instância do logger para registrar logs.
        idade (Union[str, int]): A idade da pessoa.
    Returns:
        bool: True se a pessoa deve ser descartada, caso contrário False.
    """
    if isinstance(idade, int):  # Valor numérico
        return idade < 18
    elif isinstance(idade, str):  # Valor de texto
        if idade == '+18':
            return False
        elif idade == '<18':
            return True
    else:
        return False


def filtra_escolaridade(logger, valor):
    """
    Verifica se a escolaridade é válida (Ensino Médio Completo ou superior).
    Retorna True se a escolaridade passar, False caso contrário.
    Args:
        valor (str): Valor da escolaridade a ser avaliado.
        logger (logging.Logger, optional): Logger para registrar informações. Default é None.
    Returns:
        bool: False se a escolaridade passar, True caso contrário.
    """
    if not isinstance(valor, str) or pd.isnull(valor) or valor.strip() == "":
        return False
    valor = normalize_text(valor).lower()
    if "fundamental" in valor:
        return True
    return False


def exclui_nao_recomendados(logger, df):
    cols = ["Descarte Cidade", "Descarte Telefone Invalido", "Descarte Contagem CPF",
            "Descarte Contagem Telefone", "Descarte Idade", "Descarte Escolaridade",
            "Descarte Atendimento Ativo", "Descarte Sucesso 30 Dias", "Descarte 7 Dias"]

    inf = "Descarte de Leads:\n"

    # usa só colunas que existem
    cols_validas = [c for c in cols if c in df.columns]

    for col in cols_validas:
        df[col] = df[col].fillna(False).astype(bool)
        inf += f"{col.upper():<30}{int(df[col].sum()):>10}\n"

    # remove leads que tenham QUALQUER descarte = True
    if cols_validas:
        df = df[~df[cols_validas].any(axis=1)]

    logger.debug(inf)
    return df



def divide_planilhas(logger, mailing, central_path, prefixo):
    """
    Divide o mailing em várias planilhas com base na coluna 'Planilha'.
    Cada planilha será limitada a um arquivo de 100 partes, sendo subdividido se necessário.
    Args:
        logger: Instância do logger para registrar logs.
        mailing (pd.DataFrame): DataFrame do mailing.
        central_path: Caminho de salvamento das planilhas.
        prefixo: Prefixo para o nome dos arquivos gerados.
    Returns:
        list: Lista de DataFrames correspondentes às planilhas geradas.
    """
    logger.debug("Iniciando gravação das planilhas")
    logger.debug("Selecionando colunas")
    mailing = mailing[["Nome Limpo", "CPF Limpo", "Telefone Limpo", "Telefone 2 Limpo",
                       "Fonte Limpa", "Modalidade da Entrevista", "Cidade", "Planilha"]]
    mailing.columns = ["NOME", "NUM_CPF", "NUM_TEL_1", "NUM_TEL_2",
                       "OR_FK_FONTE_ROTULO", "MODALIDADE_ENTREVISTA", "CIDADE", "Planilha"]
    mailing["NUM_CPF"] = mailing["NUM_CPF"].map(
        lambda cpf: "" if pd.isna(cpf) else f"{int(cpf):011d}")
    mailing["NUM_TEL_1"] = mailing["NUM_TEL_1"].map(
        lambda cpf: "" if pd.isna(cpf) else f"{int(cpf)}")
    mailing["NUM_TEL_2"] = mailing["NUM_TEL_2"].map(
        lambda cpf: "" if pd.isna(cpf) else f"{int(cpf)}")
    for col in ['NOME', 'CIDADE']:
        mailing[col] = mailing[col].map(lambda x: limpa_nome(logger, x))
    salva_csv_por_planilha(logger, mailing, central_path, prefixo)


def format_cpf(cpf):
    """
    Formata um CPF para o formato padrão com 11 dígitos.
    Args:
        cpf (str ou float): O CPF a ser formatado.
    Returns:
        str: O CPF formatado.
    """
    if pd.isna(cpf) or cpf == "":
        return None
    elif isinstance(cpf, str):
        if filter_numbers(cpf) not in (None, ""):
            return f"{int(filter_numbers(cpf)):011d}"
        else:
            return None
    else:
        return f"{int(cpf):011d}"


def map_functions_cols(logger, df, column_functions):
    """
    Aplica funções específicas às colunas de um DataFrame com base em um mapeamento.
    Se a coluna original não existir, cria a coluna original e a nova com valores em branco.
    Args:
        logger: Instância do logger para registrar logs.
        df (pd.DataFrame): DataFrame contendo os dados.
        column_functions (dict): Dicionário de funções a serem aplicadas às colunas.
    Returns:
        pd.DataFrame: DataFrame com as funções aplicadas
    """
    logger.debug("Aplicando funções às colunas do DataFrame")
    for col, func in column_functions.items():
        original_col = func[1]
        if original_col not in df.columns:
            logger.debug(
                f"Coluna '{original_col}' não encontrada. Criando coluna '{original_col}' e '{col}' com valores em branco.")
            df[original_col] = None
            df[col] = None
        else:
            logger.debug(
                f"Aplicando função '{func[0].__name__}' à coluna '{original_col}'")
            df[col] = df[original_col].apply(lambda x: func[0](logger, x))
    return df


def conta_ocorrencia_incremental(logger, df, col):
    """
    Conta ocorrências de valores em uma coluna de forma incremental.
    Args:
        logger: Instância do logger para registrar logs.
        df (pd.DataFrame): DataFrame contendo os dados.
        col (str): Nome da coluna a ser contada.
    Returns:
        pd.Series: Série contendo a contagem incremental
    """
    logger.debug(f"Contando ocorrências de valores na coluna '{col}'")
    return (df.groupby(col).cumcount() + 1).fillna(1).astype(int)


def limpa_cidade(logger, cidade: Optional[str]) -> str:
    """
    Limpa e padroniza o nome da cidade.
    Args:
        logger (logging.Logger): Logger para registrar informações e depuração.
        cidades_validas (list): Lista de cidades válidas para validação.
        cidade (Optional[str]): O nome da cidade a ser limpo.
    Returns:
        str: O nome padronizado da cidade:
             - "uberlandia" se a entrada for vazia ou None.
             - O nome da cidade correspondente se estiver na lista de cidades válidas (case insensitive).
             - "outra" caso contrário.
    """
    if not cidade or pd.isna(cidade):
        return "uberlandia"
    cidades_validas = config["cidades"]
    cidade_limpa = clean_text(cidade).lower()
    for cidade_valida in cidades_validas:
        if cidade_valida.lower() in cidade_limpa:
            return cidade_valida
    return "outra"


def processar_leads(logger, df):
    """
    Processa e limpa os dados de leads aplicando funções específicas para cada coluna.
    Args:
        logger (logging.Logger): Logger para registrar informações e depuração.
        df (pd.DataFrame): DataFrame contendo os dados dos leads.
    Returns:
        pd.DataFrame: DataFrame atualizado com as colunas processadas e limpas.
    """
    logger.debug("Iniciando o processamento e limpeza dos dados de leads.")
    # Dicionário de funções específicas para colunas
    column_functions: Dict[str, Callable[[str], Any]] = {
        "Email Limpo": (valida_email, "Email"),
        "Nome Limpo": (limpa_nome, "Nome"),
        "CPF Limpo": (valida_cpf, "CPF"),
        "Idade Limpo": (valida_idade, "Idade"),
        "Escolaridade Limpo": (limpa_escolaridade, "Escolaridade"),
        "Endereco Limpo": (padronizar_endereco, "Endereco"),
        "Cidade de Origem Limpo": (limpa_cidade, "Cidade de Origem"),
        "Cidade da Vaga Limpo": (limpa_cidade, "Cidade da Vaga"),
        "Telefone Limpo": (limpar_telefone, "Telefone"),
        "Telefone 2 Limpo": (limpar_telefone, "Telefone 2"),
        "Matricula Indicador Limpo": (limpa_matricula, "Matricula Indicador"),
        "Nome Indicador Limpo": (limpa_nome, "Nome Indicador"),
    }
    logger.debug(
        "Aplicando funções de limpeza e validação às colunas do DataFrame.")
    df = map_functions_cols(logger, df, column_functions)
    logger.debug(
        "Processamento e limpeza dos dados de leads concluídos com sucesso.")
    return df


def data_source_sort(logger, df, date_col='Data Form'):
    """
    Ordena o DataFrame pela coluna de data, ajustando horários 00:00:00 para 23:59:59 do mesmo dia.
    Args:
        logger (logging.Logger): Logger para registrar informações e depuração.
        df (pd.DataFrame): DataFrame contendo os dados a serem ordenados.
        date_col (str): Nome da coluna de data.
    Returns:
        pd.DataFrame: DataFrame ordenado pela coluna de data.
    """
    logger.debug(f"Ordenando o DataFrame pela coluna de data '{date_col}'")
    df[date_col] = pd.to_datetime(df[date_col])
    df[date_col] = df[date_col].where(
        df[date_col].dt.time != pd.to_datetime('00:00:00').time(),
        df[date_col] + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
    )
    return df.sort_values(date_col)


def calcula_colunas_extras(logger, df, turno, fontes):
    """
    Adiciona colunas complementares ao DataFrame fornecido.
    Args:
        logger (logging.Logger): Logger para registrar informações e depuração.
        df (pd.DataFrame): DataFrame contendo os dados a serem processados.
    Returns:
        pd.DataFrame: DataFrame atualizado com as colunas complementares adicionadas.
    """
    logger.debug(
        "Adicionando a coluna 'Fonte Limpa' com o mapping da configuração")
    df = map_fonte(logger, df, "Fonte", fontes)
    logger.debug("Adicionando a coluna 'Data Captacao' com a data atual.")
    df = add_date_column(logger, df, "Data Captacao")
    logger.debug(
        "Adicionando a coluna 'Datetime de Execução' com a data e hora atuais.")
    df = add_runtime_column(logger, df)
    logger.debug(
        "Combinando as colunas 'Cidade da Vaga Limpo' e 'Cidade de Origem Limpo' em uma única coluna 'Cidade'.")
    df = combina_cidade(
        logger, df, ["Cidade da Vaga Limpo", "Cidade de Origem Limpo"])
    logger.debug("Adicionando a coluna 'Data do Exame' com valores nulos.")
    df["Data do Exame"] = None
    logger.debug("Adicionando a coluna 'Flag Cvortex' com o valor padrão 's'.")
    df["Flag Cvortex"] = 's'
    logger.debug("Adicionando a coluna 'Codigo Fonte' com o valor padrão '2'.")
    df["Codigo Fonte"] = "2"
    logger.debug(
        "Adicionando a coluna 'Contagem CPF' com a contagem incremental de ocorrências de CPF.")
    df['Contagem CPF'] = conta_ocorrencia_incremental(logger, df, "CPF Limpo")
    logger.debug(
        "Adicionando a coluna 'Contagem Telefone' com a contagem incremental de ocorrências de telefone.")
    df['Contagem Telefone'] = conta_ocorrencia_incremental(
        logger, df, "Telefone Limpo")
    df['Modalidade da Entrevista'] = 'ONLINE'
    df['Turno'] = turno.upper()
    return df


def calcula_criterios_descarte(logger, df, cidades):
    """
    Calcula os critérios de descarte para os registros no DataFrame.
    Adiciona colunas indicando os registros que devem ser descartados com base em critérios específicos.
    Args:
        logger (logging.Logger): Logger para registrar informações e depuração.
        df (pd.DataFrame): DataFrame contendo os dados a serem processados.
    Returns:
        pd.DataFrame: DataFrame atualizado com as colunas de critérios de descarte.
    """
    logger.debug("Calculando 'Descarte Telefone Invalido'.")
    df['Descarte Cidade'] = df['Cidade'].apply(
        lambda x: not any([c in clean_text(x).lower() if x else True for c in cidades]))
    df['Descarte Telefone Invalido'] = df['Telefone Limpo'].isin(["", None,])
    logger.debug("Calculando 'Descarte Contagem CPF'.")
    df['Descarte Contagem CPF'] = df['Contagem CPF'].apply(lambda x: x != 1)
    logger.debug("Calculando 'Descarte Contagem Telefone'.")
    df['Descarte Contagem Telefone'] = df['Contagem Telefone'].apply(
        lambda x: x != 1)
    logger.debug("Calculando 'Descarte Idade'.")
    df["Descarte Idade"] = df["Idade Limpo"].map(
        lambda x: filtra_idade(logger, x) if "Idade Limpo" in df.columns else None)
    logger.debug("Calculando 'Descarte Escolaridade'.")
    df["Descarte Escolaridade"] = df["Escolaridade Limpo"].map(
        lambda x: filtra_escolaridade(logger, x) if "Escolaridade Limpo" in df.columns else None)
    return df


def bloqueio_historico(row):
    motivo = row['MOTIVO ']
    data = row["DATA TRATATIVA"]
    if row['FLAG FINALIZADO '] != 1:
        return 'Em Atendimento'
    elif (motivo == 'Contato COM Sucesso') and (pd.Timestamp.today() <= data + pd.Timedelta(days=30)):
        return 'Agendado 30 Dias'
    elif (pd.Timestamp.today() <= data + pd.Timedelta(days=7)):
        return '7 Dias'
    else:
        return 'Liberado'


def get_history_blocks(logger, leads, input_path):
    logger.info(
        "Lendo o arquivo de histórico do R&S (isso pode levar um tempo)."
    )

    relatorio = pd.read_excel(
        input_path + "/Recursos Humanos - Analitico Casos.xlsx",
        sheet_name="Tratativas",
        skiprows=6,
        parse_dates=[
            'DATA',
            'DATA CADASTRO',
            'DATA TRATATIVA',
            'DATA ENCERRAMENTO'
        ]
    )

    logger.info(f"Arquivo lido com {len(relatorio)} linhas.")
    logger.info("Processando o histórico do R&S.")

    relatorio = relatorio[
        (relatorio['FLAG ULTIMA TRATATIVA'] == 1) &
        (relatorio['FILA'] != "Receptivo")
    ]

    # 🔥 CORREÇÃO CRÍTICA AQUI
    def limpa_tel_hist(x):
        numeros = filter_numbers(x)
        if numeros == "":
            return None
        return int(numeros)

    relatorio['TELEFONE CONTATO'] = relatorio['TELEFONE CONTATO'].apply(limpa_tel_hist)

    # Remove registros sem telefone após limpeza
    relatorio = relatorio.dropna(subset=['TELEFONE CONTATO'])

    relatorio = relatorio.loc[
        relatorio.groupby('TELEFONE CONTATO')['DATA TRATATIVA'].idxmax()
    ]

    relatorio['Relatorio'] = relatorio.apply(bloqueio_historico, axis=1)

    relatorio['Telefone Limpo'] = relatorio['TELEFONE CONTATO'].apply(
        lambda x: f"{int(x):011d}"
    )

    relatorio['Descarte Atendimento Ativo'] = relatorio['Relatorio'] == 'Em Atendimento'
    relatorio['Descarte Sucesso 30 Dias'] = relatorio['Relatorio'] == 'Agendado 30 Dias'
    relatorio['Descarte 7 Dias'] = relatorio['Relatorio'] == '7 Dias'

    relatorio = relatorio[
        [
            'Telefone Limpo',
            'Descarte Atendimento Ativo',
            'Descarte Sucesso 30 Dias',
            'Descarte 7 Dias'
        ]
    ].groupby("Telefone Limpo").any().reset_index()

    logger.debug("Mesclando com o DataFrame de leads.")

    leads = pd.merge(leads, relatorio, on='Telefone Limpo', how='left')

    for col in [
        'Descarte Atendimento Ativo',
        'Descarte Sucesso 30 Dias',
        'Descarte 7 Dias'
    ]:
        leads[col] = leads[col].fillna(False)

    return leads


import math

def salva_csv_por_planilha(
    logger,
    df,
    out_path,
    file_name,
    max_linhas=100
):
    """
    Divide os CSVs por Planilha (cidade/fonte) permitindo definir
    quantos arquivos IGUAIS serão gerados por cidade,
    respeitando o limite máximo de 100 linhas por arquivo.
    """

    logger.debug("Iniciando divisão customizada por cidade/planilha")

    for planilha in sorted(df["Planilha"].unique()):
        sub_df = df[df["Planilha"] == planilha].drop(columns=["Planilha"])
        total_linhas = len(sub_df)

        if total_linhas == 0:
            continue

        # Pergunta ao usuário
        while True:
            try:
                qtd_arquivos = int(input(
                    f"Planilha '{planilha}' possui {total_linhas} linhas.\n"
                    f"Em quantos arquivos deseja dividir? "
                ))
                if qtd_arquivos <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Digite um número inteiro válido maior que zero.")

        # Calcula tamanho ideal
        tamanho_chunk = math.ceil(total_linhas / qtd_arquivos)

        # Aplica limite máximo
        if tamanho_chunk > max_linhas:
            logger.warning(
                f"Tamanho calculado ({tamanho_chunk}) excede o limite de "
                f"{max_linhas}. Ajustando automaticamente."
            )
            tamanho_chunk = max_linhas
            qtd_arquivos = math.ceil(total_linhas / tamanho_chunk)

        logger.info(
            f"Gerando {qtd_arquivos} arquivos para '{planilha}' "
            f"com até {tamanho_chunk} linhas cada."
        )

        for i in range(qtd_arquivos):
            inicio = i * tamanho_chunk
            fim = inicio + tamanho_chunk
            chunk = sub_df.iloc[inicio:fim]

            if chunk.empty:
                continue

            file_path = (
                f"{out_path}/"
                f"{file_name}_{planilha}_parte_{i + 1}.csv"
            )

            logger.debug(f"Salvando arquivo: {file_path}")
            chunk.to_csv(file_path, index=False, sep=";")



def fmt_descarte(descarte):
    return descarte.replace("Descarte ", "").replace("Contagem", "Ctg").replace("Telefone", "Tel.").replace("Atendimento", "Ctt")


def print_descarte(logger, df, prefixo):
    colunas_descartes = ['Descarte Cidade', 'Descarte Telefone Invalido', 'Descarte Contagem CPF',
                         'Descarte Contagem Telefone', 'Descarte Idade', 'Descarte Escolaridade',
                         'Descarte Atendimento Ativo', 'Descarte Sucesso 30 Dias', 'Descarte 7 Dias']
    # Cria uma nova coluna para o primeiro critério de descarte
    df['Descarte'] = df[colunas_descartes].apply(
        lambda row: fmt_descarte(row.index[row.eq(True)][0]) if row.eq(True).any() else None, axis=1)
    # Mapeia as cidades printando a matriz de descarte
    for cidade in config['cidades']:
        logger.debug(f"Mapeando os descartes de {cidade}")
        sub = df[df['Cidade'] == cidade]
        if len(sub) == 0:
            continue
        # Adiciona a quantidade bruta de linhas para cada Fonte Limpa
        qtd = sub.groupby('Fonte Limpa')[
            'Fonte Limpa'].agg({('Brutos', 'count')})
        qtd_limpo = sub[sub['Descarte'].isna()].groupby(
            'Fonte Limpa')['Fonte Limpa'].agg({('Limpos', 'count')})
        pivot_df = sub.pivot_table(
            index='Fonte Limpa',
            columns='Descarte',
            aggfunc='size',
            fill_value=0
        )
        res = pivot_df.join(qtd, how='outer').join(
            qtd_limpo, how='outer').fillna(0).astype(int)
        # Reorder columns based on colunas_descartes
        m = res[['Brutos'] + [fmt_descarte(desc) for desc in colunas_descartes if fmt_descarte(
            desc) in pivot_df.columns] + ['Limpos']]
        m = m.sort_values(["Brutos", "Limpos"], ascending=False)
        m.loc['TOTAL'] = m.sum()
        logger.debug(f"Dataframe da cidade {cidade}\n{m}")
        df_to_png(logger, m, f"Relatório de Leads da cidade de {cidade.capitalize()} no dia {datetime.now().strftime("%d/%m/%Y")}",
                  f"{prefixo}_Relatorio_{cidade.upper()}")
    logger.info("Relatórios salvos com sucesso")


def df_to_png(logger, df, legenda, filename):
    """
    Salva um DataFrame como imagem PNG com título e legenda, ajustando largura e altura automaticamente.
    Parâmetros:
    - df: pandas.DataFrame
    - legenda: str, legenda abaixo da tabela
    - filename: str, nome do arquivo de saída (default: 'tabela.png')
    """
    # Incluir índice como coluna
    df = df.reset_index().rename(columns={'index': 'Fonte'})
    # Estimar largura de cada coluna com base no texto mais longo
    col_widths = [max(df[col].astype(str).map(len).max(),
                      len(str(col))) * 0.13 for col in df.columns]
    total_width = sum(col_widths)
    fig_height = len(df) * 0.2 + 2  # altura proporcional ao número de linhas
    # Criar figura
    fig, ax = plt.subplots(figsize=(total_width, fig_height))
    ax.axis('off')
    # Título
    plt.title("People Analytics", fontsize=24, fontweight='bold',
              loc='center', pad=10, fontname='Impact', color='#2B436C')
    # Tabela
    tabela = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc='center',
        cellLoc='center',
        colLoc='center'
    )
    # Aplicar cores nas colunas
    n_cols = len(df.columns)
    for (row, col), cell in tabela.get_celld().items():
        cell.set_edgecolor('#bababa')  # Linha Cinza
        if row == len(df):
            cell.set_facecolor('#6F6F6E')  # Cinza
            cell.set_text_props(color='white', weight='bold')
        elif row == 0:
            # Cabeçalho: azul escuro com texto branco
            cell.set_facecolor('#2B436C')  # Azul escuro
            cell.set_text_props(color='white', weight='bold')
        else:
            if col == 0:
                cell.set_facecolor('#2B436C')  # Azul escuro
                cell.set_text_props(color='white')
            elif col == 1:
                cell.set_facecolor('#31ACE3')  # Azul
            elif col == n_cols - 1:
                cell.set_facecolor('#CBD742')  # Verde
            else:
                cell.set_facecolor('#ffffff')  # Branco
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(12)
    tabela.scale(1, 1.5)
    # Ajustar largura das colunas
    for i in range(len(df.columns)):
        tabela.auto_set_column_width(i)
    # Legenda
    plt.figtext(0.5, 0.01, legenda, wrap=True,
                horizontalalignment='center', fontsize=10, style='italic')
    # Ajustar margens para remover espaços em branco
    plt.subplots_adjust(top=0.88, bottom=0.08)
    # Salvar imagem
    plt.savefig(config['report_path']+filename,
                bbox_inches='tight', dpi=300)
    plt.close()
    logger.debug(f"Imagem salva como '{filename}'")


def salva_db(logger, df):
    resposta = input(
        "Deseja salvar esta planilha no banco de dados? (s/n): ").strip().lower()
    if resposta == 's':
        engine = create_engine(
            'postgresql://postgres:nova_senha@10.33.3.201:5432/db_peopleanalitycs')
        df.to_sql("leads_temp", engine, if_exists="append", index=False)
        logger.info("Dados inseridos no banco com sucesso!")
    else:
        logger.info("Salvamento no banco cancelado.")
