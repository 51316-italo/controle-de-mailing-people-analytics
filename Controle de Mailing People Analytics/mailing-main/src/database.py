from sqlalchemy import create_engine
import pandas as pd


def cria_conexao(logger, host="10.33.3.201", port="5432",
                 database="db_peopleanalitycs", user="postgres",
                 password="nova_senha"):
    try:
        # Criar a string de conexão
        engine = create_engine(
            f'postgresql://{user}:{password}@{host}:{port}/{database}')
        logger.info(
            f"Conexão com o banco de dados {database} estabelecida com sucesso.")
        return engine
    except Exception as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
        return None


# Ler uma tabela para um DataFrame
# df = pd.read_sql_table('nome_da_tabela', engine)
#
# Inserir um DataFrame de volta no banco
# df.to_sql('tb_teste', engine, if_exists='append', index=False)
