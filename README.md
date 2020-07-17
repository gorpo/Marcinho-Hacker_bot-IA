[![Build](https://img.shields.io/badge/dev-gorpo-brightgreen.svg)]()
[![Stage](https://img.shields.io/badge/Release-Stable-brightgreen.svg)]()
[![Build](https://img.shields.io/badge/python-v3.7-blue.svg)]()
[![Build](https://img.shields.io/badge/windows-7%208%2010-blue.svg)]()
[![Build](https://img.shields.io/badge/Linux-Ubuntu%20Debian-orange.svg)]()
[![Build](https://img.shields.io/badge/arquiterura-64bits-blue.svg)]()
<h2 align="center">Marcinho Hacker Telegram Heroku Bot</h2>
<img src="https://github.com/gorpoorko/Marcinho-Hacker_bot-IA/blob/master/arquivos/marcinho.jpg" alt="Marcinho um salve para você caso esteja vendo este git" width=100%>
<h2>Instruções:</h2><br>
1. Edite no arquivo config se quer rodar o bot local ou no heroku, comente e descomente as linhas.<br>
2. Edite requeriments.txt caso tenha adicionado novas libs.<br>
3. Especifique a versão do python no arquivo runtime, confira as versões de python disponiveis no heroku https://devcenter.heroku.com/articles/python-runtimes<br>
4. Crie um bot no Botfather e pegue o token do bot.<br>
5. insira este bot em um canal e pegue o id do canal, ele servirá para os logs.<br>
6. pegue sua id ela servirá para você ser adm master.<br>
<br>
<h2>Via linha de comando - CLI</h2><br>
<code>cd manicomio_bot_heroku</code><br>
<code>heroku login</code><br>
<code>heroku create --region us manicomio</code> seta us como regiao e nome_do_app defina o nome do  app no heroku<br>
<code>git init</code><br>
<code>git add *</code><br>
<code>git commit -m "Primeiro commit!"</code><br>
<code>heroku git:remote -a manicomio</code><br>


<code>git push heroku master</code>              deploy do programa no heroku<br>
<code>heroku config:set TELEGRAM_TOKEN=1186597860:AAHZTQT--xYhNHhkO8SbxlSxrdwVnkvi38s</code> seta as config vars, insira seu token<br>
<code>heroku config:set LOGS=-1001215401730</code> seta a id do canal de logs que o bot ja deve estar e ter admin<br>
<code>heroku config:set SUDOERS=522510051</code> seta o sudo ou seja adm master do bot<br>
<code>heroku ps:scale bot=1</code> start bot dyno - inicia seu bot<br>
<code>heroku logs --tail</code> tiva os logs no terminal ou cmd<br>
<code>heroku ps:stop bot</code> para o bot dyno  - para seu bot<br>


<h1> ============ GIT ====================== </h1><br>
<b>email:</b><br>
	<code>git config --global user.email "gorpoorko@protonmail.com"</code><br>
<b>username:</b><br>
	<code>git config --global user.name "gorpoorko"</code><br>
<p>----------------------------------------------------------------------------------</p><br>
<b>Adicionar um arquivo em específico</b><br>
	<code>git add meu_arquivo.txt</code><br>
<b>Adicionar um diretório em específico</b><br>
	<code>git add meu_diretorio</code><br>
<b>Adicionar todos os arquivos/diretórios</b><br>
	<code>git add .	</code><br>
<b>Adicionar um arquivo do gitignore -  git add -f arquivo_no_gitignore.txt</b><br>
<p>----------------------------------------------------------------------------------</p><br>
<b>Comitar um arquivo</b><br>
	<code>git commit meu_arquivo.txt</code><br>
<b>Comitar vários arquivos</b><br>
	<code>git commit meu_arquivo.txt meu_outro_arquivo.txt</code><br>
<b>Comitar informando mensagem</b><br>
	<code>git commit meuarquivo.txt -m "minha mensagem de commit"</code><br>
<p>----------------------------------------------------------------------------------</p><br>
<b>Remover arquivo</b><br>
	<code>git rm meu_arquivo.txt</code><br>
<b>Remover diretório</b><br>
	<code>git rm -r diretorio</code><br>
<p>----------------------------------------------------------------------------------</p><br>
<b>O primeiro push de um repositório deve conter o nome do repositório remoto e o branch.</b><br>
	<code>git push -u origin master</code><br>
<b>Os demais pushes não precisam dessa informação</b><br>
	<code>git push</code><br>
<b>Atualizar repositório local de acordo com o repositório remoto</b><br>
<b>Atualizar os arquivos no branch atual</b><br>
	<code>git pull</code><br>
<b>Buscar as alterações, mas não aplica-las no branch atual</b><br>
	<code>git fetch</code><br>
<p>----------------------------------------------------------------------------------</p><br>
<b>Criando um novo branch</b><br>
	<code>git branch bug-123</code><br>
	<code>git branch gh-pages    - para sites</code><br>
<b>Trocando para um branch existente</b><br>
	<code>git checkout bug-123</code><br>
<b>Neste caso, o ponteiro principal HEAD esta apontando para o branch chamado bug-123.</b><br>
<b>Criar um novo branch e trocar</b><br>
	<code>git checkout -b bug-456</code><br>
<b>Voltar para o branch principal (master)</b><br>
	<code>git checkout master</code><br>
<p>----------------------------------------------------------------------------------</p><br>
<b>Upando algo para um branch ja existente</b><br>
	<code>git remote add origin <"link do git seja master ou branch"></code><br>
<b>Adicione os arquivos</b><br>
	<code>git add . ou nome do arquivo ou pasta</code><br>
<b>Comente oque foi adicionado</b><br>
	<code>git commit -m "comentario"</code><br>
<b>Fazer as atualizações no repositorio online</b><br>
	<code>git fetch</code><br>
<b>Adicionando a historia do repositorio online</b><br>
	<code>git pull origin master --allow-unrelated-histories</code><br>
<p>----------------------------------------------------------------------------------</p><br>
<b>Resolver merge entre os branches</b><br>
	<code>git merge bug-123</code><br>
<b>Para realizar o merge, é necessário estar no branch que deverá receber as alterações. O merge pode automático ou manual. O merge automático será feito em arquivos textos que não sofreram alterações nas mesmas linhas, já o merge manual será feito em arquivos textos que sofreram alterações nas mesmas linhas. A mensagem indicando um merge manual será:<br>
Automerging meu_arquivo.txt<br>
CONFLICT (content): Merge conflict in meu_arquivo.txt<br>
Automatic merge failed; fix conflicts and then commit the result.</b><br>
<b>Apagando um branch</b><br>
	<code>git branch -d bug-123</code><br>
<b>Listar branches</b><br>
	<code>git branch</code><br>
<b>Listar branches com informações dos últimos commits</b><br>
	<code>git branch -v</code><br>
<b>Listar branches que já foram fundidos (merged) com o master</b><br>
	<code>git branch --merged</code><br>
<b>Listar branches que não foram fundidos (merged) com o master</b><br>
	<code>git branch --no-merged</code><br>
<p>----------------------------------------------------------------------------------</p><br>
<b>Criando um branch remoto com o mesmo nome</b><br>
	<code>git push origin bug-123</code><br>
<b>Criando um branch remoto com nome diferente</b><br>
	<code>git push origin bug-123:new-branch</code><br>
<b>Baixar um branch remoto para edição</b><br>
	<code>git checkout -b bug-123 origin/bug-123</code><br>
<b>Apagar branch remoto</b><br>
	<code>git push origin:bug-123</code><br>
<b>Fazendo o rebase entre um o branch bug-123 e o master.</b><br>
	<code>git checkout experiment</code><br>
	<code>git rebase master</code><br>
<p>----------------------------------------------------------------------------------</p><br>
<br><br>
<h2>links uteis</h2><br>
- https://devcenter.heroku.com/articles/dynos<br>
- https://devcenter.heroku.com/articles/config-vars<br>
- https://devcenter.heroku.com/articles/heroku-redis<br>
- https://devcenter.heroku.com/articles/error-codes<br>

<br>
<h2>Deploying via Heroku Dashboard</h2><br>
https://dashboard.heroku.com<br>
1. Fork este repositorio.<br>
3. Vá para https://dashboard.heroku.com, faça login, Pressione _Novo_ e escolha _Criar novo aplicativo._<br>
4. Preencha um _App Name_ e escolha _Runtime Region._<br>
5. Conecte seu repositório GitHub na página _Deploy_.<br>
6. Configuração ** Automatics deploys ** _ (Opcionalmente) ._<br>
7. _Implante uma filial do GitHub._<br>
8. Em seguida, vá para uma página _Settings_, clique em _Reveal Config Vars_ e adicione seus próprios, por exemplo:<br>
    8.1 TELEGRAM_TOKEN=118232260:AAHZTQT--xYhNHhkOsdfbxlSxrdwVnkvi38s <br>
    8.2 LOGS=-10012154123123 #id do canal do bot<br>
    8.3 SUDOERS=234234234234 #sua id<br>
9. ** Finalmente **, vá para a página _Resources_.<br>
    1. Instale o _Heroku Redis_ add-on _ (Opcionalmente) _<br>
    2. Pressione um botão pequeno da caneta, mova o controle deslizante e clique em _Confirmar_, que iniciará o bot dyno.<br>
    3. Simplesmente mova o controle deslizante para trás se precisar parar o bot dyno, lembre-se de clicar em _Confirmar_.<br>
    4. Se, por algum motivo, não estiver funcionando, verifique os logs.<br>
