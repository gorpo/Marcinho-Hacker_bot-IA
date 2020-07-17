import telepot
import random
import time
import speech_recognition as sr
from pydub import AudioSegment
import sys
import os
import dropbox
import re
import wikipedia
import sqlite3

#v3 foi inserido o sistema que proibe certas palavras

#token Bot----------------------------------------->
token_bot = '1096480409:AAFzGpjzy8OViK_AgOZJTJv_nHaieTUd104'
#token dropbox: https://www.dropbox.com/developers/apps
token_dropbox = 'qkZ0vNG8-yAAAAAAAAAbzVLfdP5vdx64GEdmlc1YcugJowBDHmXbDR3-wiM0xvQo'
#variaveis primarias ------------>
d = dropbox.Dropbox(token_dropbox)
bot = telepot.Bot(token_bot)
bot.deleteWebhook()

def criaTabelas():
    try:
        conexao_sqlite = sqlite3.connect('bot_db.sqlite')
        cursor_sqlite = conexao_sqlite.cursor()
        cursor_sqlite.execute("""  CREATE TABLE IF NOT EXISTS comandos   (int_id integer not null primary key autoincrement, tipo varchar(5000), comando varchar(5000), resposta varchar(5000));  """)
        cursor_sqlite.execute(f"""INSERT INTO comandos(int_id,tipo,comando,resposta)VALUES(1,'texto','oi','Olá Brow, como você vai?')""")
        cursor_sqlite.execute("""  CREATE TABLE IF NOT EXISTS perguntas  (int_id integer not null primary key autoincrement, usuario varchar(5000), pergunta varchar(5000));  """)
        cursor_sqlite.execute("""  CREATE TABLE IF NOT EXISTS mensagens  (int_id integer not null primary key autoincrement, 'tipo' TEXT, mensagem TEXT);  """)
        cursor_sqlite.execute("""  CREATE TABLE IF NOT EXISTS frequencia  (valor int);  """)
        cursor_sqlite.execute("""  CREATE TABLE IF NOT EXISTS proibido (termo varchar(5000));  """)
        cursor_sqlite.execute("""INSERT INTO frequencia VALUES(10)""")
        conexao_sqlite.commit()
        conexao_sqlite.close()

    except:
        pass
def frequenciaInicial():
    conexao_sqlite = sqlite3.connect('bot_db.sqlite')
    cursor_sqlite = conexao_sqlite.cursor()
    cursor_sqlite.execute(f"""INSERT INTO frequencia(valor)VALUES('1')""")
    conexao_sqlite.commit()
    conexao_sqlite.close()

def funcaoBot(msg):
    # FUNÇÕES DO BOT------------------------------------>
    content_type, chat_type, chat_id = telepot.glance(msg)
    conexao_sqlite = sqlite3.connect('bot_db.sqlite')
    conexao_sqlite.row_factory = sqlite3.Row
    cursor_sqlite = conexao_sqlite.cursor()
## SISTEMA DE FALA AUTOMATICA DO BOT COM BASE NOS POSTS DOS USUARIOS SQLITE3------------------------------------------->
    try:
        if msg.get('sticker'):
            id_sticker = msg['sticker']['file_id']
            cursor_sqlite.execute(f"""INSERT INTO mensagens(int_id,tipo,mensagem)VALUES(null,'sticker','{id_sticker}')""")
            conexao_sqlite.commit()
        if msg.get('photo'):
            id_foto = msg['photo'][0]['file_id']
            cursor_sqlite.execute(f"""INSERT INTO mensagens(int_id,tipo,mensagem)VALUES(null,'imagem','{id_foto}')""")
            conexao_sqlite.commit()
        if msg.get('document'):
            id_documento = msg['document']['file_id']
            cursor_sqlite.execute(f"""INSERT INTO mensagens(int_id,tipo,mensagem)VALUES(null,'documento','{id_documento}')""")
            conexao_sqlite.commit()
        if msg.get('audio'):
            id_audio = msg['audio']['file_id']
            cursor_sqlite.execute(f"""INSERT INTO mensagens(int_id,tipo,mensagem)VALUES(null,'audio','{id_audio}')""")
            conexao_sqlite.commit()
        if msg.get('video'):
            id_video = msg['video']['file_id']
            cursor_sqlite.execute(f"""INSERT INTO mensagens(int_id,tipo,mensagem)VALUES(null,'video','{id_video}')""")
            conexao_sqlite.commit()
        if msg.get('voice'):
            id_voz = msg['voice']['file_id']
            bot.download_file(msg['voice']['file_id'], 'arquivos/audio_usuario_db.ogg')
            sound = AudioSegment.from_file("arquivos/audio_usuario_db.ogg")
            sound.export("arquivos/audio_usuario_db.wav", format="wav", bitrate="128k")
            r = sr.Recognizer()
            with sr.WavFile('arquivos/audio_usuario_db.wav') as source:
                audio = r.record(source)
            texto = r.recognize_google(audio, language='pt-BR')
            bot.sendMessage(chat_id, f"`{msg['from']['first_name']} disse:`\n```{texto}```", 'markdown', reply_to_message_id=msg['message_id'])
            cursor_sqlite.execute(f"""INSERT INTO mensagens(int_id,tipo,mensagem)VALUES(null,'texto','{texto}')""")
            conexao_sqlite.commit()
        if msg.get('text'):#ALTERAR A FREQUENCIA DO BOT------------------------------------------------------------------------------>
            texto = msg['text']
            cursor_sqlite.execute(f"""INSERT INTO mensagens(int_id,tipo,mensagem)VALUES(null,'texto','{texto}')""")
            if texto.startswith('frequencia'):
                valor = texto[11:]
                cursor_sqlite.execute(f"""  INSERT INTO frequencia(valor)VALUES('{valor}')""")
                conexao_sqlite.commit()
                if int(valor) == 0:
                    bot.sendMessage(chat_id,f'🤖 `Frequencia alterada para {valor}, estou mutado so irei reponder comandos cadastrados`','markdown')
                if int(valor) == 1:
                    bot.sendMessage(chat_id, f'🤖 `Frequencia alterada para {valor}, vou tentar falar pouco`','markdown')
                if int(valor) > 2:
                    bot.sendMessage(chat_id, f'🤖 `Frequencia alterada para {valor}, vou falar bastante`\nCaso queira que eu pare de falar defina a frequencia como 1 e para eu falar menos defina frequencia como 2.','markdown')
            cursor_sqlite.execute("""SELECT * FROM frequencia; """)
            frequencia_sqlite = cursor_sqlite.fetchall()
            try:
                contador = int(random.randint(0, frequencia_sqlite[-1][0] * 2)) - 1
                frequencia = int(frequencia_sqlite[-1][0])
            except:
                contador = random.randint(0, 1)
                frequencia = 1
                pass
            if contador < frequencia:  # se o contador for menor que a frequencia o bot entrara na conversa enviando alguma mensagem salva no banco de dados
                pass                   # print(f'🚫 Não enviou: contador:{int(contador)}     - menor que a frequencia setada: {frequencia }')
            else:                      # print(f'🤖 Bot enviou: contador:{int(contador)} maior/igual que a frequencia setada: {frequencia}')
                cursor_sqlite.execute("""SELECT * FROM mensagens; """)
                mensagens_sqlite = cursor_sqlite.fetchall()
                quantidade_mensagens = len(mensagens_sqlite)
                randomico = random.randint(0,   quantidade_mensagens - 1)  # fornece um numero randomico para pegarmos as mensagens na db
                m = mensagens_sqlite[randomico][2]
                tipo_mensagem = mensagens_sqlite[randomico][1]
                if m.startswith('frequencia') or m.startswith('#') or m.startswith('comandos') or m.startswith('%') or m.startswith('$') or m.startswith('/help') or m.startswith('permitir') or m.startswith('proibir') or m.startswith('proibidas'):
                    pass
                else:#SISTEMA DE RESPOSTA AUTOMATICA COM BASE NA VARIAVEL "tipo" DA DATABASE-------------------------------->
                    if tipo_mensagem == 'imagem':
                        bot.sendPhoto(chat_id, photo= m)
                        print(f'🤖 Bot enviou uma imagem no grupo {msg["chat"]["title"]} com a id {m}')
                    if tipo_mensagem == 'documento':
                        bot.sendDocument(chat_id, document=m)
                        print(f'🤖 Bot enviou um documento no grupo {msg["chat"]["title"]} com a id {m}')
                    if tipo_mensagem == 'audio':
                        bot.sendAudio(chat_id, audio=m)
                        print(f'🤖 Bot enviou um audio no grupo {msg["chat"]["title"]} com a id {m}')
                    if tipo_mensagem == 'video':
                        bot.sendVideo(chat_id, video= m)
                        print(f'🤖 Bot enviou um video no grupo {msg["chat"]["title"]} com a id {m}')
                    if tipo_mensagem == 'texto':
                        bot.sendMessage(chat_id, m)
                        print(f'🤖 Bot enviou no grupo {msg["chat"]["title"]}: {m}')
                    if tipo_mensagem == 'sticker':
                        bot.sendSticker(chat_id, sticker=m)
                        print(f'🤖 Bot enviou sticker no grupo {msg["chat"]["title"]} com a id {m}')
    except Exception as e:
        print(f'Erro no sistema de fala automatica: {e}')
        pass










# SISTEMA QUE DELETA MENSAGENS PROIBIDAS --------------------------------------------------------------------->
    try:#verifica se a palavra é proibida, se for deleta a mensagem do usuario e envia um aviso------>
        cursor_sqlite.execute("""SELECT * FROM proibido; """)
        mensagens_proibidas = cursor_sqlite.fetchall()
        for mensagem in mensagens_proibidas:
            if mensagem['termo'] in texto:
                if texto.lower().startswith('permitir'):
                    pass
                else:
                    identificador = telepot.message_identifier(msg)
                    bot.deleteMessage(identificador)
                    bot.sendMessage(chat_id,f"@{msg['from']['username']} `você usou uma palavra proibida, não fale bosta aqui!`", 'markdown')

        if msg.get('text'):
            texto = msg['text']
            if texto.lower().startswith('proibir'):#proibe as palavras e as cadastra na Database------------------------------->
                palavra_proibida = texto[8:]
                if palavra_proibida.lower() == 'proibir' or palavra_proibida.lower() == '' or palavra_proibida.lower() == ' ' or palavra_proibida.lower() == '#' or palavra_proibida.lower() == '$' or palavra_proibida.lower() == '%' or palavra_proibida.lower() == '' or palavra_proibida.lower() == 'comandos' or palavra_proibida.lower() == '/help' or palavra_proibida.lower() == 'fale sobre' or palavra_proibida.lower() == 'frequencia':
                    pass
                    print('sem chance')
                else:
                    cursor_sqlite.execute(f"""INSERT INTO proibido VALUES('{palavra_proibida}')""")
                    conexao_sqlite.commit()
                    bot.sendMessage(chat_id, f'🤖🚫 `Proibido:`***{palavra_proibida}***\nPara voltar permitir esta palavra use o comando `permitir`, para ver palavras proibidas use `proibidas`', 'markdown', reply_to_message_id=msg['message_id'])
            if texto.lower().startswith('permitir'):#permite novamente as palavras e as descadastra na Database------------------------------->
                palavra_permitida = texto[9:]
                cursor_sqlite.execute(f"""DELETE FROM proibido WHERE termo='{palavra_permitida}'""")
                conexao_sqlite.commit()
                bot.sendMessage(chat_id,f'🤖✔️ `Permitido:`***{palavra_permitida}***\nPara voltar proibir esta palavra use o comando `proibir`, para ver palavras proibidas use `proibidas`','markdown', reply_to_message_id=msg['message_id'])
            if texto.lower().startswith('proibidas'):#lista as palavras proibidas cadastradas  na Database------------------------------->
                cursor_sqlite.execute("""SELECT * FROM proibido; """)
                mensagens_proibidas = cursor_sqlite.fetchall()
                todas_proibidas = []
                separador = ' \n'
                for result in mensagens_proibidas:
                    todas_proibidas.append(result['termo'])
                bot.sendMessage(chat_id, f'🤖 `Palavras Proibidas:`\n ***{separador.join(map(str, todas_proibidas))}***','markdown', reply_to_message_id=msg['message_id'])
                bot.sendMessage(chat_id,'Para proibir use `proibir` e para permitir use `permitir`','markdown')


    except Exception as e:
        print(e)
#COMANDOS INSERIDOS MANUALMENTE NA PROGRAMAÇAO--------------------------------------------------------------->
    if msg.get('text'):
        texto = msg['text']
        id_mensagem = msg['message_id']
        id_user = msg['from']['id']
        nome = msg['from']['username']
        try:
            # print(f"Usuário: @{msg['from']['username']} | Grupo: {msg['chat']['title']} | Mensagem: {texto}")
            if texto == 'amigo':
                bot.sendVideo(chat_id, video=open('arquivos/marcinho.mp4', 'rb'), reply_to_message_id=msg['message_id'])
            # sistema que uso para xingar----->
            quantidade = texto[0:2]
            comando_falar = texto[2]
            frase_cortada = texto[4:]
            if comando_falar == 'x':
                if int(quantidade) > 20:
                    bot.sendMessage(chat_id, 'Estou limitado a floodar somente 20x no maximo!', 'markdown')
                else:
                    for i in range(int(quantidade)):
                        bot.sendMessage(chat_id, f'***{frase_cortada}***', 'markdown')
        except:
            pass

#SISTEMA DE RESPOSTA COM BASE NOS COMANDOS CADASTRADOS MANUALMENTE NO GRUPO | CRUD--------------------------------------------------->
        try:
            cursor_sqlite.execute("""SELECT * FROM comandos; """)
            resultados = cursor_sqlite.fetchall()
            for resultado in resultados:
                comando = resultado['comando']
                resposta = resultado['resposta']
                tipo = resultado['tipo']
                if tipo == 'texto' and comando == texto.lower():
                    bot.sendMessage(chat_id, f"{resposta}", reply_to_message_id=msg['message_id'])
                if tipo == 'imagem' and comando == texto.lower():
                    bot.sendPhoto(chat_id, photo=resposta, reply_to_message_id=msg['message_id'])
                if tipo == 'voz' and comando == texto.lower():
                    bot.sendVoice(chat_id, voice=resposta, reply_to_message_id=msg['message_id'])
                if tipo == 'audio' and comando == texto.lower():
                    bot.sendAudio(chat_id, audio=resposta, reply_to_message_id=msg['message_id'])
                if tipo == 'documento' and comando == texto.lower():
                    bot.sendDocument(chat_id, document=resposta, reply_to_message_id=msg['message_id'])
                if tipo == 'video' and comando == texto.lower():
                    bot.sendVideo(chat_id, video=resposta, reply_to_message_id=msg['message_id'])
        except:
            pass

#SISTEMA CADASTRO DE RESPOSTAS COM BASE NOS COMANDOS CADASTRADOS MANUALMENTE NO GRUPO | CRUD----------------------------------------->
        ##SISTEMA DE CADASTRO USANDO REPLY------------------------------------------------>
        try:#IMAGENS na Database-------------------------------------------------------------->
            if 'photo' in msg.get('reply_to_message') and texto.startswith('#'):
                comando = texto[1:]
                id_foto = msg.get('reply_to_message')['photo'][0]['file_id']
                cursor_sqlite.execute("""SELECT * FROM comandos; """)
                resultados = cursor_sqlite.fetchall()
                existe_cadastro_imagem = 0  # contador para verificar se o comando ja existe
                for res in resultados:  # loop em todos resultados da Database
                    if res['comando'] == comando and 'photo' in msg.get('reply_to_message'):
                        existe_cadastro_imagem = 1  # troca o valor de existe_cadastro para 1
                if existe_cadastro_imagem == 1:
                    bot.sendMessage(chat_id, "🤖 `Comando já cadastrado, tente outro`",'markdown')
                else:
                    cursor_sqlite.execute(f"""INSERT INTO comandos (tipo,comando,resposta) VALUES ('imagem','{comando}','{id_foto}')""")
                    conexao_sqlite.commit()
                    bot.sendMessage(chat_id,f"🤖 Dados inseridos com exito.\n`Comando:` {comando}\n`File_id:` {id_foto}",'markdown')
        except:
            pass
        try:#VIDEOS na Database----------------------------------------------------------------->
            if 'video' in msg.get('reply_to_message') and texto.startswith('#'):
                comando = texto[1:]
                id_video = msg.get('reply_to_message')['video']['file_id']
                cursor_sqlite.execute("""SELECT * FROM comandos; """)
                resultados = cursor_sqlite.fetchall()
                existe_cadastro_video = 0  # contador para verificar se o comando ja existe
                for res in resultados:  # loop em todos resultados da Database
                    if res['comando'] == comando:
                        existe_cadastro_video = 1  # troca o valor de existe_cadastro para 1
                if existe_cadastro_video == 1:  # se o valor existe_cadastro esta como 1 ele avisa que ja existe cadastro
                    bot.sendMessage(chat_id, "🤖 `Comando já cadastrado, tente outro`",'markdown')
                else:
                    cursor_sqlite.execute(f"""INSERT INTO comandos (tipo,comando,resposta) VALUES ('video','{comando}','{id_video}')""")
                    conexao_sqlite.commit()
                    bot.sendMessage(chat_id,f"🤖 Dados inseridos com exito.\n`Comando:` {comando}\n`File_id:` {id_video}",'markdown')
        except:
            pass
        try:#DOCUMENTOS na Database------------------------------------------------------------->
            if 'document' in msg.get('reply_to_message') and texto.startswith('#'):
                comando = texto[1:]
                id_documento = msg.get('reply_to_message')['document']['file_id']
                cursor_sqlite.execute("""SELECT * FROM comandos; """)
                resultados = cursor_sqlite.fetchall()
                existe_cadastro_document = 0  # contador para verificar se o comando ja existe
                for res in resultados:  # loop em todos resultados da Database
                    if res['comando'] == comando:
                        existe_cadastro_document = 1  # troca o valor de existe_cadastro para 1
                if existe_cadastro_document == 1:  # se o valor existe_cadastro esta como 1 ele avisa que ja existe cadastro
                    bot.sendMessage(chat_id, "🤖 `Comando já cadastrado, tente outro`",'markdown')
                else:
                    cursor_sqlite.execute(f"""INSERT INTO comandos (tipo,comando,resposta) VALUES ('documento','{comando}','{id_documento}')""")
                    conexao_sqlite.commit()
                    bot.sendMessage(chat_id,f"🤖 Dados inseridos com exito.\n`Comando:` {comando}\n`File_id:` {id_documento}",'markdown')
        except:
            pass
        try:#AUDIOS VOZ na Database------------------------------------------------------------>
            if 'voice' in msg.get('reply_to_message') and texto.startswith('#'):
                comando = texto[1:]
                id_voz = msg.get('reply_to_message')['voice']['file_id']
                cursor_sqlite.execute("""SELECT * FROM comandos; """)
                resultados = cursor_sqlite.fetchall()
                existe_cadastro_voz = 0  # contador para verificar se o comando ja existe
                for res in resultados:  # loop em todos resultados da Database
                    # se o comando ja existir o valor existe_cadastro passa ser 1
                    if res['comando'] == comando:
                        existe_cadastro_voz = 1  # troca o valor de existe_cadastro para 1
                if existe_cadastro_voz == 1:  # se o valor existe_cadastro esta como 1 ele avisa que ja existe cadastro
                    bot.sendMessage(chat_id, "🤖 `Comando já cadastrado, tente outro`",'markdown')
                else:
                    cursor_sqlite.execute(f"""INSERT INTO comandos (tipo,comando,resposta) VALUES ('voz','{comando}','{id_voz}')""")
                    conexao_sqlite.commit()
                    bot.sendMessage(chat_id,f"🤖 Dados inseridos com exito.\n`Comando:` {comando}\n`File_id:` {id_voz}",'markdown')
        except:
            pass
        try:#AUDIOS MUSICA na Database--------------------------------------------------------->
            if 'audio' in msg.get('reply_to_message') and texto.startswith('#'):
                comando = texto[1:]
                id_audio = msg.get('reply_to_message')['audio']['file_id']
                cursor_sqlite.execute("""SELECT * FROM comandos """)
                resultados = cursor_sqlite.fetchall()
                existe_cadastro_audio = 0  # contador para verificar se o comando ja existe
                for res in resultados:  # loop em todos resultados da Database
                    if res['comando'] == comando:
                        existe_cadastro_audio = 1  # troca o valor de existe_cadastro para 1
                if existe_cadastro_audio == 1:  # se o valor existe_cadastro esta como 1 ele avisa que ja existe cadastro
                    bot.sendMessage(chat_id, "🤖 `Comando já cadastrado, tente outro`", 'markdown')
                else:
                    cursor_sqlite.execute(f"""INSERT INTO comandos (tipo,comando,resposta) VALUES ('audio','{comando}','{id_audio}')""")
                    conexao_sqlite.commit()
                    bot.sendMessage(chat_id, f"🤖 Dados inseridos com exito.\n`Comando:` {comando}\n`File_id:` {id_audio}", 'markdown')
        except:
            pass
        try:#MENSAGENS de texto na Database---------------------------------------------------------------->
            if 'text' in  msg.get('reply_to_message') and texto.startswith('#'):
                comando = texto[1:]
                id_text= msg.get('reply_to_message')['text']
                cursor_sqlite.execute("""SELECT * FROM comandos; """)
                resultados = cursor_sqlite.fetchall()
                existe_cadastro_text = 0  # contador para verificar se o comando ja existe
                for res in resultados:  # loop em todos resultados da Database
                    if res['comando'] == comando:
                        existe_cadastro_text = 1  # troca o valor de existe_cadastro para 1
                if existe_cadastro_text == 1:  # se o valor existe_cadastro esta como 1 ele avisa que ja existe cadastro
                    bot.sendMessage(chat_id, "🤖 `Comando já cadastrado, tente outro`", 'markdown')
                elif existe_cadastro_text == 0:  # se o valor de existe_cadastro nao foi alterado ele cadastra novo comando
                    cursor_sqlite.execute(f"""INSERT INTO comandos(id,'texto')VALUES('{comando}','{id_text}')""")
                    conexao_sqlite.commit()
                    bot.sendMessage(chat_id, f"`🤖 Dados inseridos com exito.\nComando:` {comando}\n`File_id:` {id_text}", 'markdown')
        except:
            pass
        try:#SISTEMA DE CADASTRO DE COMANDOS DOS USUARIOS USANDO SOMENTE O # -------------------------------------------------------------->
            if texto.startswith('#') and not msg.get('reply_to_message'):
                texto_cadastro = texto[1:].split(' ')
                comando = str(texto_cadastro[0]).lower()  # gera o texto do comando
                separador = ' '
                resposta = separador.join(map(str, texto_cadastro[1:]))
                cursor_sqlite.execute("""SELECT * FROM comandos; """)
                resultados = cursor_sqlite.fetchall()
                existe_cadastro = 0  # contador para verificar se o comando ja existe
                for res in resultados:  # loop em todos resultados da Database
                    if res['comando'] == comando:
                        existe_cadastro = 1  # troca o valor de existe_cadastro para 1
                if existe_cadastro == 1:  # se o valor existe_cadastro esta como 1 ele avisa que ja existe cadastro
                    bot.sendMessage(chat_id, "Comando já cadastrado, tente outro",  reply_to_message_id=msg['message_id'])
                else:
                    cursor_sqlite.execute(f"""INSERT INTO comandos (tipo,comando,resposta) VALUES ('texto','{comando}','{resposta}')""")
                    conexao_sqlite.commit()
                    bot.sendMessage(chat_id, f"🤖 Dados inseridos com exito.\nComando: {comando}\nResposta: {resposta}",  reply_to_message_id=msg['message_id'])
        except:
            pass
        try:#RECADASTRAMENTO DE RESPOSTAS USANDO O $--------------------------------------------------------------------------------------------------->
            if texto.startswith('$'):
                texto_cadastro = texto[1:].split(' ')
                comando = str(texto_cadastro[0]).lower()  # gera o texto do comando
                separador = ' '
                resposta = separador.join(map(str, texto_cadastro[1:])) #pega todo resto da lista e poe no separador retornando toda lista em uma linha
                cursor_sqlite.execute(f"""DELETE FROM comandos WHERE comando='{comando}'""")
                conexao_sqlite.commit()
                bot.sendMessage(chat_id, f'Comando: {comando} apagado do sistema.',  reply_to_message_id=msg['message_id'])
                cursor_sqlite.execute(f"""INSERT INTO comandos(id,'texto')VALUES('{comando}','{resposta}')""")
                conexao_sqlite.commit()
                bot.sendMessage(chat_id, f"🤖 Dados inseridos com exito.\n`Comando:` {comando}\n`Resposta:` {resposta}", 'markdown')
        except:
            pass
        try:#DELETAR COMANDOS CADASTRADOS USANDO O %------------>
            if texto.startswith('%'):
                comando = texto[1:].lower()  # tira do texto o  comando 'cadastrar'
                cursor_sqlite.execute(f"""DELETE FROM comandos WHERE comando='{comando}'""")
                conexao_sqlite.commit()
                bot.sendMessage(chat_id, f'🤖 `Comando {comando} apagado do sistema.`', 'markdown',  reply_to_message_id=msg['message_id'])
        except:
            bot.sendMessage(chat_id, f'🤖 `Comando {comando} inexistente ou ocorreu um erro.`', 'markdown',  reply_to_message_id=msg['message_id'])
        try:#LISTAR COMANDOS CADASTRADOS PELOS USUARIOS NA DATABASE------------>
            if texto.lower() == 'comandos' or texto == '/comandos':
                cursor_sqlite.execute("""SELECT * FROM comandos; """)
                resultados = cursor_sqlite.fetchall()
                todos_comandos = []
                separador = ' \n'
                for result in resultados:
                    todos_comandos.append(result['comando'])
                bot.sendMessage(chat_id, f'`Comandos cadastrados:`\n ***{separador.join(map(str,todos_comandos))}***', 'markdown', reply_to_message_id=msg['message_id'])
        except Exception as e:
            print(e)
            pass
        try:# CADASTRO PERGUNTAS DOS USUARIOS---------------------------------------------------------->
            if '??' in texto:
                usuario = f"@{msg['from']['username']}"
                cursor_sqlite.execute(f"""INSERT INTO perguntas VALUES (null,'{usuario}','{texto}')""")
                conexao_sqlite.commit()
                bot.sendMessage(chat_id, f"🤖 {msg['from']['first_name']} `sua pergunta foi cadastrada.`", 'markdown')
        except Exception as e:
            print(e)
            pass
        try:# VERIFICAR PERGUNTAS DOS USUARIOS----------------------------------------------------------->
            if texto.lower() == 'perguntas':
                cursor_sqlite.execute("""SELECT * FROM perguntas""")
                resultados = cursor_sqlite.fetchall()
                if resultados == []:
                    bot.sendMessage(chat_id, f"🤖 {msg['from']['first_name']} `não tenho perguntas cadastradas, tente outra hora ou cadastre algumas perguntas.`",'markdown')
                else:
                    for resultado in resultados:
                        usuario = resultado['usuario']
                        pergunta = resultado['pergunta']
                        bot.sendMessage(chat_id, f"`Usuário:`{usuario}\n`Pergunta:`{pergunta}", 'markdown')
        except Exception as e:
            print(e)
            pass
        try:# LIMPAR PERGUNTAS DOS USUARIOS------------------------------------------------------------->
            if texto.lower() == 'limpar perguntas':
                cursor_sqlite.execute("""DELETE FROM perguntas""")
                conexao_sqlite.commit()
                bot.sendMessage(chat_id, f"🤖 {msg['from']['first_name']} Todas perguntas foram apagadas!")
        except:
            pass

#SISTEMA DE UPLOAD PARA DROPBOX | necessario mudar o caminho para sua pasta que quer baixar os arquivos----------------------------------------------------------->
        try:#UPLOAD DE DOCUMENTOS PARA O DROPBOX
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
        try:#UPLOAD DE IMAGENS/FOTOS PARA O DROPBOX
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
        try:#SISTEMA DE RESPOSTAS COM BASE NA WIKIPEDIA---------------------------------------------------------------->
            if 'fale sobre' in texto.lower():
                termo = texto[10:]
                wikipedia.set_lang("pt")
                pesquisa = wikipedia.summary(termo)
                bot.sendMessage(chat_id, pesquisa, reply_to_message_id=msg['message_id'])
        except Exception as e:
            print(e)
            bot.sendMessage(chat_id, 'Desconheço este assunto...', reply_to_message_id=msg['message_id'])

#COMANDOS DO CHAT PRIVADO-------------------------------------------------------------------------------------------------------------------------->
    if chat_type == 'private':
        for i in range(10):
            bot.sendMessage(chat_id, 'Sai do meu privado, vai toma no cu cu mano fala comigo no grupo arrombado.')
#CONFIGURAÇÕES PARA GRUPOS----------------------------------------------------------------------------------------------------------------------------->
    if msg.get('new_chat_member'): # mensagem de boas vindas ao usuario--------------->>
        user_novo = msg.get('new_chat_member')['first_name']
        bot.sendMessage(chat_id, f"Bem vindo {user_novo} ao {msg['chat']['title']}")
    if msg.get('text') == 'restart': #sistema de reinicio do bot
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
fale sobre robôs
***SOBRE A FREQUENCIA DE MENSAGENS*** 
```Este bot envia mensagens baseado em uma frequencia que deve ser setada entre 2 e 10, onde:```
`frequencia 1 = mudo`
`frequencia 2 = fala pouco`
`frequencia 10 = fala muito`
***SOBRE PROIBIR E PERMITIR PALAVRAS***
```Este bot pode restringir e permitir palavras com os comandos:```
`proibir uma palavra:` proibir 
`permitir uma palavra:` permtir 
`ver palavras proibidas:` proibidas
"""
        bot.sendMessage(chat_id, texto, 'markdown')


#INICIA O BOT | CRIA O BANCO DE DADOS E TABELAS SQLITE-------------------------------------------------->
criaTabelas()
frequenciaInicial()
bot.message_loop(funcaoBot)
print('Bot esta online, para desativar o bot feche o programa!')
while 1:
    pass
