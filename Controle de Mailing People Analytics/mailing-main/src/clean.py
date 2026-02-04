import warnings

from utils import *
from config import config


# Ignorar warnings desnecessários
warnings.simplefilter("ignore")


def main():

    # Define parâmetros e logger
    verbose = get_run_params()
    logger = config_logger(verbose)

    # Define grupo e prefixo automaticamente
    grupo, prefixo = get_grupo_prefixo(logger, config['output_path'])

    # Ler entradas
    leads = get_all_sheets(
        logger, config['input_path'], config['sheets'], config['layouts'])
    if leads is None or len(leads) == 0:
        logger.error("Nenhum lead encontrado no arquivo de entrada.")
        return

    # Compilar leads com mapping de funções
    leads = processar_leads(logger, leads)

    # Ordenar por data despriorizando indeed (sem horario)
    leads = data_source_sort(logger, leads)

    # Calcular colunas extras para os leads
    leads = calcula_colunas_extras(logger, leads, grupo, config['fontes'])

    # Calcula as colunas de critérios de descarte
    leads = calcula_criterios_descarte(logger, leads, config['cidades'])

    # Incluir bloqueio de ultimos dias com base em tabulação do R&S
    leads = get_history_blocks(logger, leads, config['input_path'])

    # Calcular planilhas para divisão dos arquivos
    leads = decide_planilha(logger, leads, config['quebra_fonte'])

    # Salvar leads em Excel
    overwrite_excel(
        logger, leads, config['output_path'] + prefixo+"Mailing.xlsx")

    salva_db(logger, leads)

    # print_logo()

    # Limpar Leads não recomendados
    mailing = exclui_nao_recomendados(logger, leads)

    # Dividindo mailing em planilhas
    logger.debug("Dividindo mailing em planilhas")
    divide_planilhas(logger, mailing, config['central_path'], prefixo)

    # Informando sobre o resultado dos descartes
    print_descarte(logger, leads, prefixo)

    logger.info("Processo de limpeza concluído com sucesso")


if __name__ == "__main__":
    main()
