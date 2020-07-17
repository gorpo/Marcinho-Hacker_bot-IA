import pymysql.cursors
conexao = pymysql.connect(host='192.168.0.6', #localhost
                          port=3306,
                          user='gorpo',
                          password='daimonae',
                          db='marcinho_bot',
                          charset='utf8mb4',
                          cursorclass = pymysql.cursors.DictCursor)
menu = input('[1] cria tabela comandos [2] cria tabela perguntas a ser respondidas')
#tenta criar as tabelas da Database---------------->
if menu == '1':
    try:
        with conexao.cursor() as cursor:  # faz a conexao com o cursor do mysql
            tabela = f'create table comandos ({"id INT  AUTO_INCREMENT, tipo varchar(5000), comando varchar(5000), resposta varchar(5000), PRIMARY KEY (id)"})'
            cursor.execute(tabela)  # execução do comando no banco de dados
            conexao.commit()  # gravação do comando no banco de dados
            cursor.close()
        print('Tabela criada na Database com sucesso')
    except Exception as e:
        print(e)
        pass
if menu == '2':
    try:
        with conexao.cursor() as cursor:  # faz a conexao com o cursor do mysql
            tabela = f'create table perguntas ({"id INT  AUTO_INCREMENT, usuario varchar(5000),grupo varchar(5000), pergunta varchar(5000), PRIMARY KEY (id)"})'
            cursor.execute(tabela)  # execução do comando no banco de dados
            conexao.commit()  # gravação do comando no banco de dados
            cursor.close()
        print('Tabela criada na Database com sucesso')
    except Exception as e:
        print(e)
        pass
