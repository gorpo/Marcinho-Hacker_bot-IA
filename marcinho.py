import telepot
import random
import time
import speech_recognition as sr
from pydub import AudioSegment
import pymysql.cursors
import sys
import os
import dropbox
import re
import wikipedia
import sqlite3
"""
# INSTRUÇÕES PARA CONECTAR A UMA DATABASE EXTERNA:
# 1. de permissão a maquina que vai conectar no seu serviço mysql:
#    sudo mysql -u root -p
#    GRANT ALL  ON * . * TO 'seu_usuario'@'192.168.*.*' IDENTIFIED BY 'sua_senha';
#    FLUSH PRIVILEGES;
# 2. edite o arquivo de configuração do mysql:
#    sudo nano  /etc/mysql/mariadb.conf.d/50-server.cnf
# troque por:
#     bind-address  = 0.0.0.0
# 3. libere a porta para conexao externa no firewall:
#   sudo ufw allow 3306
#   sudo ufw allow 3306/tcp
#   sudo ufw allow 3306/udp
"""

#token Bot----------------------------------------->
 #No telegram vá ate o @botfather e crie um bot, pegue seu token e insira aqui
token_bot = '1096480409:AAFzGpjzy8OViK_AgOZJTJv_nHaieTUd104'

#INSTRUÇÕES PARA USO DO DROPBOX:
    #Crie uma conta Dropbox, após acesse este link para pegar seu token_dropbox: https://www.dropbox.com/developers/apps
token_dropbox = 'qkZ0vNG8-yAAAAAAAAAbzVLfdP5vdx64GEdmlc1YcugJowBDHmXbDR3-wiM0xvQo'

#INSTRUÇÕES PARA EDITAR NA CONEXÃO COM A DATABASE:
    #1 - crie um banco de dados mysql e insira seus dados nas variavel "banco_dados_mysql" abaixo...
    #2 - Insira o hostname ou ip em host_mysql, Ex: 192.168.0.3 ou localhost ambos funcionam
    #3 - Insira seu nome de usuario do Mysql na variavel usuario_mysql
    #4 - Insira sua senha de usuario do Mysql na variavel senha_mysql
banco_dados_mysql = 'marcinho_bot'
host_mysql = 'localhost'
usuario_mysql = 'gorpo'
senha_mysql = 'daimonae'


#variaveis primarias ------------>
d = dropbox.Dropbox(token_dropbox)
bot = telepot.Bot(token_bot)
bot.deleteWebhook()
conexao = pymysql.connect(host= host_mysql, port=3306, user=usuario_mysql, password=senha_mysql, db=banco_dados_mysql, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


def criaTabelas():
    try: #sistema que cria duas tabelas para receber os dados que vão ser cadastrados.
        with conexao.cursor() as cursor:  # faz a conexao com o cursor do mysql
            tabela_comandos = f'create table comandos ({"id INT  AUTO_INCREMENT, tipo varchar(5000), comando varchar(5000), resposta varchar(5000), PRIMARY KEY (id)"})'
            cursor.execute(tabela_comandos)  # execução do comando no banco de dados
            tabela_perguntas = f'create table perguntas ({"id INT  AUTO_INCREMENT, usuario varchar(5000), pergunta varchar(5000), PRIMARY KEY (id)"})'
            cursor.execute(tabela_perguntas)  # execução do comando no banco de dados
            conexao.commit()  # gravação do comando no banco de dados
            cursor.close()
            print('Tabelas criada na Database com sucesso')
    except Exception as e:
        print(f'As tabelas ja existem ou você não preencheu os dados mysql corretos, preencha os dados mysql nas linhas 42,43,44,45: Código {e}')
        pass
    try:
        conexao_sqlite = sqlite3.connect('bot.db')
        cursor_sqlite = conexao_sqlite.cursor()
        cursor_sqlite.execute("""  CREATE TABLE IF NOT EXISTS mensagens (int_id integer not null primary key autoincrement, mensagem TEXT);  """)
        cursor_sqlite.execute( """  CREATE TABLE IF NOT EXISTS frequencia (valor int);  """)
        conexao_sqlite.close()
    except:
        pass

def funcaoBot(msg):
    # FUNÇÕES DO BOT------------------------------------>
    content_type, chat_type, chat_id = telepot.glance(msg)
    frequencia = 0 #recebe o valor da frequencia que o bot deve falar

    if msg.get('text'):
        texto = msg['text']
        # sistema que pega as mensagens dos usuarios e retorna depois(velasco) SQLITE3---->
        conexao_sqlite = sqlite3.connect('bot.db')
        cursor_sqlite = conexao_sqlite.cursor()
        # fica injetando todas falas na database
        cursor_sqlite.execute(f"""  INSERT INTO mensagens(int_id,mensagem)VALUES(null,'{texto}')""")
        conexao_sqlite.commit()
        if texto.startswith('frequencia'):
            valor = texto[11:]
            cursor_sqlite.execute(f"""  INSERT INTO frequencia(valor)VALUES('{valor}')""")
            conexao_sqlite.commit()
            bot.sendMessage(chat_id,f'🤖 `Frequencia alterada para`:{valor}')

        cursor_sqlite.execute("""SELECT * FROM frequencia; """)
        frequencia_sqlite = cursor_sqlite.fetchall()
        contador = random.randint(0, frequencia_sqlite[-1][0] + 10)
        print(frequencia_sqlite[-1][0])
        if contador > frequencia_sqlite[-1][0]: #Quando o contador passar a frequencia ele envia uma mensagem
            # seleciona e le todas mensagens da database
            cursor_sqlite.execute("""SELECT * FROM mensagens; """)
            mensagens_sqlite = cursor_sqlite.fetchall()
            quantidade_mensagens = len(mensagens_sqlite)
            randomico = random.randint(0, quantidade_mensagens - 1) #fornece um numero randomico para pegarmos as mensagens na db
            mensagem_database_sqlite = mensagens_sqlite[randomico][1]
            bot.sendMessage(chat_id, mensagem_database_sqlite)
        print(frequencia_sqlite)







        # sistema de RESPOSTA com database-------------->
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from comandos')
                resultados = cursor.fetchall()  # pega todos resultados da db
                cursor.close()
                for resultado in resultados:
                    comando = resultado['comando']
                    resposta = resultado['resposta']
                    tipo = resultado['tipo']
                    if tipo == 'texto' and comando == texto:
                        bot.sendMessage(chat_id, f"{resposta}", reply_to_message_id=msg['message_id'])
                    if tipo == 'imagem' and comando == texto:
                        bot.sendPhoto(chat_id, photo=resposta, reply_to_message_id=msg['message_id'])
                    if tipo == 'voz' and comando == texto:
                        bot.sendVoice(chat_id, voice=resposta, reply_to_message_id=msg['message_id'])
                    if tipo == 'audio' and comando == texto:
                        bot.sendAudio(chat_id, audio=resposta, reply_to_message_id=msg['message_id'])
                    if tipo == 'documento' and comando == texto:
                        bot.sendDocument(chat_id, document=resposta, reply_to_message_id=msg['message_id'])
                    if tipo == 'video' and comando == texto:
                        bot.sendVideo(chat_id, video=resposta, reply_to_message_id=msg['message_id'])
        except:
            pass

        # sistema de RESPOSTA sem database----------------------------->
        try:
            if texto == 'oi':
                bot.sendMessage(chat_id, f"ola {msg['from']['first_name']}", reply_to_message_id=msg['message_id'])
            if texto == 'amigo':
                bot.sendVideo(chat_id, video=open('arquivos/marcinho.mp4', 'rb'), reply_to_message_id=msg['message_id'])
        except:
            pass



        #CRUD DO BOT ABAIXO, sistema de cadastro de video, imagem, audio, voz, texto e comandos personalizados----------------------------------------->
        #IMAGENS na Database------------------------------------->
        try:
            if 'photo' in msg.get('reply_to_message') and texto.startswith('#'):
                comando = texto[1:]
                id_foto = msg.get('reply_to_message')['photo'][0]['file_id']
                with conexao.cursor() as cursor:  # faz a conexao com o cursor do mysql
                    cursor.execute('select * from comandos')
                    resultados = cursor.fetchall()  # tras os resultados da tabela mysql
                    cursor.close()  # sempre fechar a conexao para nao dar erro no mysql
                    existe_cadastro_imagem = 0  # contador para verificar se o comando ja existe
                    for res in resultados:  # loop em todos resultados da Database
                        # se o comando ja existir o valor existe_cadastro passa ser 1
                        if res['comando'] == comando:
                            existe_cadastro_imagem = 1  # troca o valor de existe_cadastro para 1
                    if existe_cadastro_imagem == 1:  # se o valor existe_cadastro esta como 1 ele avisa que ja existe cadastro
                        bot.sendMessage(chat_id, "🤖 `Comando já cadastrado, tente outro`",'markdown')
                    elif existe_cadastro_imagem == 0:  # se o valor de existe_cadastro nao foi alterado ele cadastra novo comando
                        with conexao.cursor() as cursor:
                            # insere os valores na tabela
                            cursor.execute(f"insert into comandos values (id,'imagem','{comando}','{id_foto}')")
                            conexao.commit()  # gravação do comando no banco de dados
                            cursor.close()
                            bot.sendMessage(chat_id,f"🤖 Dados inseridos com exito.\n`Comando:` {comando}\n`File_id:` {id_foto}",'markdown')
        except:
            pass
        #VIDEOS na Database--------------------------------------->
        try:
            if  'video' in msg.get('reply_to_message') and texto.startswith('#'):
                comando = texto[1:]
                id_video = msg.get('reply_to_message')['video']['file_id']
                with conexao.cursor() as cursor:  # faz a conexao com o cursor do mysql
                    cursor.execute('select * from comandos')
                    resultados = cursor.fetchall()  # tras os resultados da tabela mysql
                    cursor.close()  # sempre fechar a conexao para nao dar erro no mysql
                    existe_cadastro_video = 0  # contador para verificar se o comando ja existe
                    for res in resultados:  # loop em todos resultados da Database
                        # se o comando ja existir o valor existe_cadastro passa ser 1
                        if res['comando'] == comando:
                            existe_cadastro_video = 1  # troca o valor de existe_cadastro para 1
                    if existe_cadastro_video == 1:  # se o valor existe_cadastro esta como 1 ele avisa que ja existe cadastro
                        bot.sendMessage(chat_id, "🤖 `Comando já cadastrado, tente outro`",'markdown')
                    elif existe_cadastro_video == 0:  # se o valor de existe_cadastro nao foi alterado ele cadastra novo comando
                        with conexao.cursor() as cursor:
                            # insere os valores na tabela
                            cursor.execute(f"insert into comandos values (id,'video','{comando}','{id_video}')")
                            conexao.commit()  # gravação do comando no banco de dados
                            cursor.close()
                            bot.sendMessage(chat_id,f"🤖 Dados inseridos com exito.\n`Comando:` {comando}\n`File_id:` {id_video}",'markdown')
        except:
            pass
        #DOCUMENTOS na Database-------------------------------------------->
        try:
            if 'document' in msg.get('reply_to_message') and texto.startswith('#'):
                comando = texto[1:]
                id_documento = msg.get('reply_to_message')['document']['file_id']
                with conexao.cursor() as cursor:  # faz a conexao com o cursor do mysql
                    cursor.execute('select * from comandos')
                    resultados = cursor.fetchall()  # tras os resultados da tabela mysql
                    cursor.close()  # sempre fechar a conexao para nao dar erro no mysql
                    existe_cadastro_document = 0  # contador para verificar se o comando ja existe
                    for res in resultados:  # loop em todos resultados da Database
                        # se o comando ja existir o valor existe_cadastro passa ser 1
                        if res['comando'] == comando:
                            existe_cadastro_document = 1  # troca o valor de existe_cadastro para 1
                    if existe_cadastro_document == 1:  # se o valor existe_cadastro esta como 1 ele avisa que ja existe cadastro
                        bot.sendMessage(chat_id, "🤖 `Comando já cadastrado, tente outro`",'markdown')
                    elif existe_cadastro_document == 0:  # se o valor de existe_cadastro nao foi alterado ele cadastra novo comando
                        with conexao.cursor() as cursor:
                            # insere os valores na tabela
                            cursor.execute(f"insert into comandos values (id,'documento','{comando}','{id_documento}')")
                            conexao.commit()  # gravação do comando no banco de dados
                            cursor.close()
                            bot.sendMessage(chat_id,f"🤖 Dados inseridos com exito.\n`Comando:` {comando}\n`File_id:` {id_documento}",'markdown')
        except:
            pass
        #AUDIOS VOZ na Database-------------------------------------------->
        try:
            if 'voice' in msg.get('reply_to_message') and texto.startswith('#'):
                comando = texto[1:]
                id_voz = msg.get('reply_to_message')['voice']['file_id']
                with conexao.cursor() as cursor:  # faz a conexao com o cursor do mysql
                    cursor.execute('select * from comandos')
                    resultados = cursor.fetchall()  # tras os resultados da tabela mysql
                    cursor.close()  # sempre fechar a conexao para nao dar erro no mysql
                    existe_cadastro_voz = 0  # contador para verificar se o comando ja existe
                    for res in resultados:  # loop em todos resultados da Database
                        # se o comando ja existir o valor existe_cadastro passa ser 1
                        if res['comando'] == comando:
                            existe_cadastro_voz = 1  # troca o valor de existe_cadastro para 1
                    if existe_cadastro_voz == 1:  # se o valor existe_cadastro esta como 1 ele avisa que ja existe cadastro
                        bot.sendMessage(chat_id, "🤖 `Comando já cadastrado, tente outro`",'markdown')
                    elif existe_cadastro_voz == 0:  # se o valor de existe_cadastro nao foi alterado ele cadastra novo comando
                        with conexao.cursor() as cursor:
                            # insere os valores na tabela
                            cursor.execute(f"insert into comandos values (id,'voz','{comando}','{id_voz}')")
                            conexao.commit()  # gravação do comando no banco de dados
                            cursor.close()
                            bot.sendMessage(chat_id,f"🤖 Dados inseridos com exito.\n`Comando:` {comando}\n`File_id:` {id_voz}",'markdown')
        except:
            pass
        #AUDIOS MUSICA na Database-------------------------------------------->
        try:
            if 'audio' in msg.get('reply_to_message') and texto.startswith('#'):
                comando = texto[1:]
                id_audio = msg.get('reply_to_message')['audio']['file_id']
                with conexao.cursor() as cursor:  # faz a conexao com o cursor do mysql
                    cursor.execute('select * from comandos')
                    resultados = cursor.fetchall()  # tras os resultados da tabela mysql
                    cursor.close()  # sempre fechar a conexao para nao dar erro no mysql
                    existe_cadastro_audio = 0  # contador para verificar se o comando ja existe
                    for res in resultados:  # loop em todos resultados da Database
                        # se o comando ja existir o valor existe_cadastro passa ser 1
                        if res['comando'] == comando:
                            existe_cadastro_audio = 1  # troca o valor de existe_cadastro para 1
                    if existe_cadastro_audio == 1:  # se o valor existe_cadastro esta como 1 ele avisa que ja existe cadastro
                        bot.sendMessage(chat_id, "🤖 `Comando já cadastrado, tente outro`", 'markdown')
                    elif existe_cadastro_audio == 0:  # se o valor de existe_cadastro nao foi alterado ele cadastra novo comando
                        with conexao.cursor() as cursor:
                            # insere os valores na tabela
                            cursor.execute(f"insert into comandos values (id,'audio','{comando}','{id_audio}')")
                            conexao.commit()  # gravação do comando no banco de dados
                            cursor.close()
                            bot.sendMessage(chat_id, f"🤖 Dados inseridos com exito.\n`Comando:` {comando}\n`File_id:` {id_audio}", 'markdown')
        except:
            pass
        #MENSAGENS na Database-------------------------------------------->
        try:
            if 'text' in  msg.get('reply_to_message') and texto.startswith('#'):
                comando = texto[1:]
                id_text= msg.get('reply_to_message')['text']
                with conexao.cursor() as cursor:  # faz a conexao com o cursor do mysql
                    cursor.execute('select * from comandos')
                    resultados = cursor.fetchall()  # tras os resultados da tabela mysql
                    cursor.close()  # sempre fechar a conexao para nao dar erro no mysql
                    existe_cadastro_text = 0  # contador para verificar se o comando ja existe
                    for res in resultados:  # loop em todos resultados da Database
                        # se o comando ja existir o valor existe_cadastro passa ser 1
                        if res['comando'] == comando:
                            existe_cadastro_text = 1  # troca o valor de existe_cadastro para 1
                    if existe_cadastro_text == 1:  # se o valor existe_cadastro esta como 1 ele avisa que ja existe cadastro
                        bot.sendMessage(chat_id, "🤖 `Comando já cadastrado, tente outro`", 'markdown')
                    elif existe_cadastro_text == 0:  # se o valor de existe_cadastro nao foi alterado ele cadastra novo comando
                        with conexao.cursor() as cursor:
                            # insere os valores na tabela
                            cursor.execute(f"insert into comandos values (id,'texto','{comando}','{id_text}')")
                            conexao.commit()  # gravação do comando no banco de dados
                            cursor.close()
                            bot.sendMessage(chat_id, f"`🤖 Dados inseridos com exito.\nComando:` {comando}\n`File_id:` {id_text}", 'markdown')
        except:
            pass
        #CADASTRO de RESPOSTAS para o BOT ------------>
        if texto.startswith('#') and not msg.get('reply_to_message'):
            texto_cadastro = texto[1:].split(' ')
            comando = str(texto_cadastro[0]).lower()  # gera o texto do comando
            separador = ' '
            resposta = separador.join(map(str, texto_cadastro[1:]))
            with conexao.cursor() as cursor:              # faz a conexao com o cursor do mysql
                try:
                    # seleciona tudo na tabela usuarios
                    cursor.execute('select * from comandos')
                    resultados = cursor.fetchall()  # tras os resultados da tabela mysql
                    cursor.close()  # sempre fechar a conexao para nao dar erro no mysql
                    existe_cadastro = 0  # contador para verificar se o comando ja existe
                    for res in resultados:  # loop em todos resultados da Database
                        # se o comando ja existir o valor existe_cadastro passa ser 1
                        if res['comando'] == comando:
                            existe_cadastro = 1  # troca o valor de existe_cadastro para 1
                    if existe_cadastro == 1:  # se o valor existe_cadastro esta como 1 ele avisa que ja existe cadastro
                        bot.sendMessage(chat_id, "Comando já cadastrado, tente outro",  reply_to_message_id=msg['message_id'])
                    elif existe_cadastro == 0:  # se o valor de existe_cadastro nao foi alterado ele cadastra novo comando
                        with conexao.cursor() as cursor:
                            # insere os valores na tabela
                            cursor.execute(f"insert into comandos values (id,'texto','{comando}','{resposta}')")
                            conexao.commit()                   # gravação do comando no banco de dados
                            cursor.close()
                            bot.sendMessage(chat_id, f"🤖 Dados inseridos com exito.\nComando: {comando}\nResposta: {resposta}",  reply_to_message_id=msg['message_id'])
                except:
                    pass
        #RECADASTRO de respostas------------>
        try:
            if texto.startswith('$'):
                texto_cadastro = texto[1:].split(' ')
                comando = str(texto_cadastro[0]).lower()  # gera o texto do comando
                separador = ' '
                resposta = separador.join(map(str, texto_cadastro[1:])) #pega todo resto da lista e poe no separador retornando toda lista em uma linha

                with conexao.cursor() as cursor:
                    # executa o codigo mysql no banco de dados
                    cursor.execute(f"DELETE FROM comandos WHERE comando='{comando}'")
                    conexao.commit()  # grava o codigo no banco de dados
                    cursor.close()
                    bot.sendMessage(chat_id, f'Comando: {comando} apagado do sistema.',  reply_to_message_id=msg['message_id'])
                with conexao.cursor() as cursor:
                    # insere os valores na tabela
                    cursor.execute(f"insert into comandos values (id,'texto','{comando}','{resposta}')")
                    conexao.commit()  # gravação do comando no banco de dados
                    cursor.close()
                    bot.sendMessage(chat_id, f"🤖 Dados inseridos com exito.\n`Comando:` {comando}\n`Resposta:` {resposta}", 'markdown')
        except:
            pass

        #DELETAR respostas------------>
        if texto.startswith('%'):
            comando = texto[1:].lower()  # tira do texto o  comando 'cadastrar'
            try:
                with conexao.cursor() as cursor:
                    # executa o codigo mysql no banco de dados
                    cursor.execute( f"DELETE FROM comandos WHERE comando='{comando}';")
                    conexao.commit()  # grava o codigo no banco de dados
                    cursor.close()
                    bot.sendMessage(chat_id, f'🤖 `Comando {comando} apagado do sistema.`', 'markdown',  reply_to_message_id=msg['message_id'])
            except:
                bot.sendMessage(chat_id, f'🤖 `Comando {comando} inexistente ou ocorreu um erro.`', 'markdown',  reply_to_message_id=msg['message_id'])

        #LISTAR comandos------------>
        if texto.lower() == 'comando':
            try:
                with conexao.cursor() as cursor:  # faz a conexao com o cursor do mysql
                    # seleciona tudo na tabela usuarios
                    cursor.execute('select * from comandos')
                    resultados = cursor.fetchall()  # tras os resultados da tabela mysql
                    cursor.close()  # sempre fechar a conexao para nao dar erro no mysql
                    todos_comandos = []
                    separador = ' \n'
                    for result in resultados:
                        todos_comandos.append(result['comando'])
                # separador.join(map(str, todos_comandos)) descompacta lista em uma coisa so
                bot.sendMessage(chat_id, f'`Comandos cadastrados:`\n ***{separador.join(map(str,todos_comandos))}***', 'markdown', reply_to_message_id=msg['message_id'])
            except Exception as e:
                print(e)
                pass
        # CADASTRO PERGUNTAS DOS USUARIOS---------------------------------------------------------->
        try:
            if '?' in texto:
                with conexao.cursor() as cursor:
                    usuario = f"@{msg['from']['username']}"
                    cursor.execute(f"insert into perguntas values (id,'{usuario}','{texto}')")
                    conexao.commit()  # gravação do comando no banco de dados
                    cursor.close()
                    bot.sendMessage(chat_id, f"🤖 {msg['from']['first_name']} `sua pergunta foi cadastrada.`",
                                    'markdown')
        except Exception as e:
            print(e)
            pass

        # VERIFICAR PERGUNTAS DOS USUARIOS------------------->
        try:
            if texto.lower() == 'perguntas':
                with conexao.cursor() as cursor:  # faz a conexao com o cursor do mysql
                    cursor.execute('select * from perguntas')
                    resultados = cursor.fetchall()  # tras os resultados da tabela mysql
                    cursor.close()  # sempre fechar a conexao para nao dar erro no mysql
                    if resultados == ():
                        bot.sendMessage(chat_id,
                                        f"🤖 {msg['from']['first_name']} `não tenho perguntas cadastradas, tente outra hora ou cadastre algumas perguntas.`",
                                        'markdown')
                    else:
                        for resultado in resultados:
                            usuario = resultado['usuario']
                            pergunta = resultado['pergunta']
                            bot.sendMessage(chat_id, f"`Usuário:`{usuario}\n`Pergunta:`{pergunta}", 'markdown')
        except:
            pass
        # LIMPAR PERGUNTAS DOS USUARIOS------------------->
        try:
            if texto.lower() == 'limpar perguntas':
                with conexao.cursor() as cursor:  # faz a conexao com o cursor do mysql
                    cursor.execute('TRUNCATE TABLE perguntas')
                    resultados = cursor.fetchall()  # tras os resultados da tabela mysql
                    cursor.close()  # sempre fechar a conexao para nao dar erro no mysql
                    bot.sendMessage(chat_id, f"🤖 {msg['from']['first_name']} Todas perguntas foram apagadas!")
        except:
            pass

        # SISTEMA DROPBOX----------------------------------------------------------->
        #upload documentos dropbox
        try:
            if 'document' in msg.get('reply_to_message') and texto.lower().startswith('dropbox'):
                id_arquivo = msg.get('reply_to_message')['document']['file_id']
                nome_arquivo = msg.get('reply_to_message')['document']['file_name']
                tamanho = msg.get('reply_to_message')['document']['file_size']
                if tamanho > 10000000:
                    bot.sendMessage(chat_id, '🤖 `Tamanho maximo para envio de 10mb`', 'markdown', reply_to_message_id=msg['message_id'])
                if tamanho < 10000000:
                    bot.download_file(id_arquivo, f'arquivos/{nome_arquivo}')
                    bot.sendMessage(chat_id,f"🤖 `{msg['from']['first_name']} acabei de baixar seu arquivo, vou upar ele para o Dropbox`",'markdown', reply_to_message_id=msg['message_id'])
                    targetfile = f"/GDRIVE_TCXSPROJECT/MARCINHO_BOT/{nome_arquivo}"
                    with open(f'arquivos/{nome_arquivo}', "rb") as f:
                        meta = d.files_upload(f.read(), targetfile, mode=dropbox.files.WriteMode("overwrite"))
                    link = d.sharing_create_shared_link(targetfile)
                    url = link.url
                    dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
                    bot.sendMessage(chat_id, f"🤖 `{msg['from']['first_name']} acabei upar seu arquivo no Dropbox`\nlink:{dl_url}", 'markdown', reply_to_message_id=msg['message_id'])
                    os.remove(f'arquivos/{nome_arquivo}')
        except:
            pass
    #upload fotos dropbox
        try:
            if 'photo' in msg.get('reply_to_message') and texto.lower().startswith('dropbox'):
                id_arquivo = msg.get('reply_to_message')['photo'][0]['file_id']
                nome_arquivo = id_arquivo[0:5]
                bot.download_file(id_arquivo, f'arquivos/{nome_arquivo}.jpg')
                bot.sendMessage(chat_id,f"🤖 `{msg['from']['first_name']} acabei de baixar seu arquivo, vou upar ele para o Dropbox`",'markdown', reply_to_message_id=msg['message_id'])
                targetfile = f"/GDRIVE_TCXSPROJECT/MARCINHO_BOT/{nome_arquivo}.jpg"
                time.sleep(1)
                with open(f'arquivos/{nome_arquivo}.jpg', "rb") as f:
                    meta = d.files_upload(f.read(), targetfile, mode=dropbox.files.WriteMode("overwrite"))
                link = d.sharing_create_shared_link(targetfile)
                url = link.url
                dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
                bot.sendMessage(chat_id, f"🤖 `{msg['from']['first_name']} acabei upar seu arquivo no Dropbox`\nlink:{dl_url}", 'markdown', reply_to_message_id=msg['message_id'])
                os.remove(f'arquivos/{nome_arquivo}.jpg')
        except:
            pass
        #SISTEMA DE RESPOSTAS COM BASE NA WIKIPEDIA---------------->
        if 'fale sobre' in texto.lower():
            try:
                termo = texto[10:]
                wikipedia.set_lang("pt")
                pesquisa = wikipedia.summary(termo)
                bot.sendMessage(chat_id, pesquisa, reply_to_message_id=msg['message_id'])
            except Exception as e:
                print(e)
                bot.sendMessage(chat_id, 'Desconheço este assunto...', reply_to_message_id=msg['message_id'])


    # transcodifica vox em texto, recebendo audio do usuario e reenviando em texto no grupo--------------------------------------------------------------->
    if content_type == 'voice':  # or msg.get('reply_to_message')
        try:
            bot.download_file(msg['voice']['file_id'], 'arquivos/audio_usuario.ogg')
            sound = AudioSegment.from_file("arquivos/audio_usuario.ogg")
            sound.export("arquivos/audio_usuario.wav", format="wav", bitrate="128k")
            r = sr.Recognizer()
            with sr.WavFile('arquivos/audio_usuario.wav') as source:
                audio = r.record(source)
            texto = r.recognize_google(audio, language='pt-BR')
            bot.sendMessage(chat_id, f"`{msg['from']['first_name']} disse:`\n```{texto}```", 'markdown',reply_to_message_id=msg['message_id'])
        except Exception as e:
            print(e)
            pass

    # CONFIGURAÇÕES PARA GRUPOS------------------------->
    # mensagem de boas vindas ao usuario--------------->>
    if msg.get('new_chat_member'):
        user_novo = msg.get('new_chat_member')['first_name']
        bot.sendMessage(chat_id, f"Bem vindo {user_novo} ao {msg['chat']['title']}")
    if msg.get('text') == 'restart':
        bot.sendMessage(chat_id, '🤖`reiniciado...`\nMe envie um "oi" para ver se voltei', 'markdown')
        os.execl(sys.executable, sys.executable, *sys.argv)

    if msg.get('text') == '/help':
        texto = """
***CADASTRO DE COMANDOS E REPOSTAS NA DATABASE***        
🤖`Para cadastrar um comando no banco de dados:`
#comando resposta que o usuário vai receber
🤖`Para recadastrar um comando no banco de dados:`
$comando resposta que o usuário vai receber
🤖`Para deletar um comando`
%comando 
***CADASTRO DE PERGUNTA DOS USUARIOS*** 
```Sempre que um usuário enviar alguma pergunta com o ponto de interrogação ela será cadastrada na Database```
🤖`Para ver as perguntas feitas pelo usuario digite:`
perguntas 
🤖`Para limpar as perguntas da Database digite:`
limpar perguntas
***EXTRAS***
🤖`Se usar a palavra dropbox como reposta em documentos e imagens eu farei o upload para seu dropbox`
🤖`Pergunte ao bot com o comando:`
fale sobre robôs"""
        bot.sendMessage(chat_id, texto, 'markdown')


#INICIA O BOT-------------------------------------------------->
#cria as tabelas no mysql, caso existam ignora e inicia o bot-->
# chama a função e deixa o bot em um loop para ficar ativo----->>
criaTabelas()
bot.message_loop(funcaoBot)
print('Bot esta online, para desativar o bot feche o programa!')
while 1:
    pass
