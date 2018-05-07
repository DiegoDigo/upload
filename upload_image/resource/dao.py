import psycopg2


def atualizar_produto(url_produto: str, codigo_produto: str, conn: psycopg2) -> None:
    cursor = conn.cursor()
    cursor.execute("""update cadastro_produto set path_imagem = '{}' 
                      where codigo_erp = '{}'""".format(url_produto, codigo_produto))
    conn.commit()
    conn.close()


def salvar_url_produto(url_produto: str, codigo_produto: int):
    try:
        connect_str = "dbname='portal_vendas_6461' " \
                      "user='postgres'" \
                      "host='localhost'" \
                      "port='5432'" \
                      "password='control'"
        atualizar_produto(url_produto, str(codigo_produto), psycopg2.connect(connect_str))
    except Exception as e:
        print(e)
