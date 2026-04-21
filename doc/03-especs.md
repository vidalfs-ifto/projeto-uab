# Especificação do Sistema de Atendimento

## 1. Configurações e Ambiente

/requirements.txt

- ação: criar
- descrição: Arquivo de dependências contendo as bibliotecas necessárias para a execução do sistema em ambiente Python.
- pseudocódigo:
  Flask==3.0.0
  Flask-SQLAlchemy==3.1.1
  Authlib==1.2.1
  python-dotenv==1.0.0
  gunicorn==21.2.0

/.env.example

- ação: criar
- descrição: Template para as variáveis de ambiente necessárias para a configuração e provisionamento inicial do sistema.
- pseudocódigo:
  SECRET_KEY=string_aleatoria_segura
  DATABASE_PATH=app/db/atendimento.db
  PROPRIETARIO_EMAIL=proprietario@empresa.com
  PROPRIETARIO_PASSWORD=senha_segura_inicial
  DEBUG_MODE=True ou False
  GOOGLE_CLIENT_ID=id_oauth_google
  GOOGLE_CLIENT_SECRET=secret_oauth_google

/config.py

- ação: criar

- descrição: Módulo de configuração que carrega as variáveis de ambiente e define as configurações globais da aplicação Flask.

- pseudocódigo:
  IMPORTAR os
  IMPORTAR dotenv
  EXECUTAR dotenv.load_dotenv()
  CLASSE Config:
  
      DEFINIR SECRET_KEY COMO os.getenv("SECRET_KEY")
      DEFINIR SQLALCHEMY_DATABASE_URI COMO "sqlite:///" CONCATENADO COM os.getenv("DATABASE_PATH")
      DEFINIR DEBUG COMO BOOLEANO(os.getenv("DEBUG_MODE"))
      DEFINIR PROPRIETARIO_EMAIL COMO os.getenv("PROPRIETARIO_EMAIL")
      DEFINIR PROPRIETARIO_PASSWORD COMO os.getenv("PROPRIETARIO_PASSWORD")

## 2. Inicialização e Infraestrutura

/app/database.py

- ação: criar

- descrição: Inicialização da instância do SQLAlchemy responsável pelo mapeamento objeto-relacional (ORM).

- pseudocódigo:
  IMPORTAR SQLAlchemy DE flask_sqlalchemy
  INSTANCIAR db = SQLAlchemy()

/app/__init__.py

- ação: criar

- descrição: Função de fábrica (factory) da aplicação Flask. Responsável por inicializar extensões e registrar blueprints (controladores).

- pseudocódigo:
  IMPORTAR Flask
  IMPORTAR Config DE config
  IMPORTAR db DE app.database
  FUNCAO create_app():
  
      INSTANCIAR app = Flask(__name__)
      CARREGAR_CONFIGURACOES(app, Config)
      
      INICIALIZAR_EXTENSAO(db, app)
      
      REGISTRAR_BLUEPRINT(app, auth_controller)
      REGISTRAR_BLUEPRINT(app, usuario_controller)
      REGISTRAR_BLUEPRINT(app, ticket_controller)
      REGISTRAR_BLUEPRINT(app, relatorio_controller)
      
      RETORNAR app

/run.py

- ação: criar

- descrição: Ponto de entrada da aplicação. Garante a criação do banco de dados e do proprietário inicial caso não existam.

- pseudocódigo:
  IMPORTAR create_app DE app
  IMPORTAR db DE app.database
  IMPORTAR UsuarioModel DE app.models
  IMPORTAR Config DE config
  INSTANCIAR app = create_app()
  SE_ARQUIVO_EXECUTADO_DIRETAMENTE:
  
      COM CONTEXTO_DA_APLICACAO(app):
          CRIAR_TABELAS_BANCO_DE_DADOS(db)
      
          ATRIBUIR proprietario = BUSCAR_USUARIO_POR_EMAIL(Config.PROPRIETARIO_EMAIL)
          SE proprietario NAO EXISTE:
              CRIAR novo_proprietario COMO UsuarioModel(email=Config.PROPRIETARIO_EMAIL, role="PROPRIETARIO")
              novo_proprietario.set_senha(Config.PROPRIETARIO_PASSWORD)
              SALVAR_NO_BANCO(novo_proprietario)
      
      INICIAR_SERVIDOR(app, host="0.0.0.0", port=5000)

/Dockerfile

- ação: criar
- descrição: Definição da imagem do container para empacotamento da aplicação.
- pseudocódigo:
  DEFINIR_IMAGEM_BASE python:3.10-slim
  DEFINIR_DIRETORIO_TRABALHO /app
  COPIAR requirements.txt PARA .
  EXECUTAR pip install -r requirements.txt
  COPIAR todo_conteudo PARA .
  EXPOR_PORTA 5000
  DEFINIR_COMANDO_INICIAL ["python", "run.py"]

## 3. Camada de Dados (Models)

/app/models/usuario_model.py

- ação: criar

- descrição: Definição da entidade de usuários unificada, utilizando um campo 'role' para determinar os privilégios.

- pseudocódigo:
  IMPORTAR db DE app.database
  CLASSE UsuarioModel(db.Model):
  
      DEFINIR_NOME_TABELA "usuarios"
      
      COLUNA id COMO INTEIRO, CHAVE_PRIMARIA
      COLUNA nome COMO TEXTO, NAO_NULO
      COLUNA email COMO TEXTO, UNICO, NAO_NULO
      COLUNA senha_hash COMO TEXTO, NAO_NULO
      COLUNA role COMO ENUM("PROPRIETARIO", "ADMINISTRADOR", "ATENDENTE", "CLIENTE"), NAO_NULO
      COLUNA criado_por_id COMO INTEIRO, CHAVE_ESTRANGEIRA("usuarios.id"), NULO_PERMITIDO
      
      METODO set_senha(senha_plana):
          ATRIBUIR self.senha_hash = GERAR_HASH_CRIPTOGRAFICO(senha_plana)
      
      METODO check_senha(senha_plana):
          RETORNAR COMPARAR_HASH(self.senha_hash, senha_plana)

/app/models/ticket_model.py

- ação: criar

- descrição: Definição da entidade de solicitações (tickets) criadas pelos clientes e respondidas pelos atendentes.

- pseudocódigo:
  IMPORTAR db DE app.database
  CLASSE TicketModel(db.Model):
  
      DEFINIR_NOME_TABELA "tickets"
      
      COLUNA id COMO INTEIRO, CHAVE_PRIMARIA
      COLUNA cliente_id COMO INTEIRO, CHAVE_ESTRANGEIRA("usuarios.id"), NAO_NULO
      COLUNA atendente_id COMO INTEIRO, CHAVE_ESTRANGEIRA("usuarios.id"), NULO_PERMITIDO
      COLUNA assunto COMO TEXTO, NAO_NULO
      COLUNA descricao COMO TEXTO, NAO_NULO
      COLUNA status COMO ENUM("ABERTO", "EM_ANDAMENTO", "RESOLVIDO", "FECHADO"), PADRAO="ABERTO"
      COLUNA data_criacao COMO DATA_HORA, PADRAO=DATA_HORA_ATUAL
      COLUNA data_atualizacao COMO DATA_HORA, PADRAO=DATA_HORA_ATUAL, AO_ATUALIZAR=DATA_HORA_ATUAL

/app/models/log_model.py

- ação: criar

- descrição: Definição da entidade de log de operações para auditoria de ações críticas (CRUD de usuários).

- pseudocódigo:
  IMPORTAR db DE app.database
  CLASSE LogModel(db.Model):
  
      DEFINIR_NOME_TABELA "logs"
      
      COLUNA id COMO INTEIRO, CHAVE_PRIMARIA
      COLUNA usuario_autor_id COMO INTEIRO, CHAVE_ESTRANGEIRA("usuarios.id"), NAO_NULO
      COLUNA acao COMO TEXTO, NAO_NULO  // Ex: "CRIAR_ATENDENTE", "DELETAR_ADMIN"
      COLUNA entidade_afetada_id COMO INTEIRO, NULO_PERMITIDO
      COLUNA data_hora COMO DATA_HORA, PADRAO=DATA_HORA_ATUAL

## 4. Utilitários (Utils)

/app/utils/auth_utils.py

- ação: criar

- descrição: Decoradores customizados para validar autenticação e autorização baseada em roles nas rotas.

- pseudocódigo:
  IMPORTAR functools
  IMPORTAR session, redirect DE flask
  FUNCAO requer_autenticacao(funcao_rota):
  
      SE "usuario_id" NAO ESTA EM session:
          RETORNAR redirect("/login")
      RETORNAR funcao_rota
  
  FUNCAO requer_roles(lista_roles_permitidas):
  
      FUNCAO decorador(funcao_rota):
          SE "usuario_role" NAO ESTA EM session OU session["usuario_role"] NAO ESTA EM lista_roles_permitidas:
              RETORNAR erro_acesso_negado (403)
          RETORNAR funcao_rota
      RETORNAR decorador

/app/utils/log_utils.py

- ação: criar

- descrição: Função utilitária para facilitar o registro de eventos no banco de dados.

- pseudocódigo:
  IMPORTAR db DE app.database
  IMPORTAR LogModel DE app.models.log_model
  FUNCAO registrar_auditoria(autor_id, acao, afetado_id):
  
      INSTANCIAR log = LogModel(usuario_autor_id=autor_id, acao=acao, entidade_afetada_id=afetado_id)
      ADICIONAR_AO_BANCO(log)
      CONFIRMAR_TRANSACAO(db)

## 5. Camada de Lógica de Negócio (Controllers)

/app/controllers/auth_controller.py

- ação: criar

- descrição: Controlador responsável pelo login, logout, registro autônomo (apenas Clientes) e OAuth.

- pseudocódigo:
  DEFINIR_BLUEPRINT auth_controller
  ROTA "/login" [GET, POST]:
  
      SE METODO == POST:
          ATRIBUIR usuario = BUSCAR_USUARIO(email=formulario.email)
          SE usuario EXISTE E usuario.check_senha(formulario.senha):
              CRIAR_SESSAO(usuario.id, usuario.role)
              RETORNAR REDIRECIONAR("/dashboard")
          RETORNAR REDIRECIONAR("/login?erro=credenciais")
      RETORNAR RENDERIZAR_TEMPLATE("auth/login.html")
  
  ROTA "/register" [GET, POST]:
  
      SE METODO == POST:
          INSTANCIAR novo_cliente = UsuarioModel(nome=formulario.nome, email=formulario.email, role="CLIENTE")
          novo_cliente.set_senha(formulario.senha)
          SALVAR_NO_BANCO(novo_cliente)
          RETORNAR REDIRECIONAR("/login")
      RETORNAR RENDERIZAR_TEMPLATE("auth/register.html")
  
  ROTA "/logout" [GET]:
  
      LIMPAR_SESSAO()
      RETORNAR REDIRECIONAR("/login")
  
  ROTA "/oauth/google" [GET]:
  
      PROCESSAR_FLUXO_AUTHLIB()
      ATRIBUIR usuario_oauth = OBTER_DADOS_GOOGLE()
      ATRIBUIR usuario = BUSCAR_USUARIO(email=usuario_oauth.email)
      SE usuario NAO EXISTE:
          CRIAR_NOVO_USUARIO(email=usuario_oauth.email, role="CLIENTE")
      CRIAR_SESSAO(usuario.id, usuario.role)
      RETORNAR REDIRECIONAR("/dashboard")

/app/controllers/usuario_controller.py

- ação: criar

- descrição: Controlador para CRUD de usuários restrito por privilégios, com obrigatoriedade de log.

- pseudocódigo:
  DEFINIR_BLUEPRINT usuario_controller
  IMPORTAR requer_autenticacao, requer_roles DE app.utils.auth_utils
  IMPORTAR registrar_auditoria DE app.utils.log_utils
  ROTA "/proprietario/usuarios" [GET, POST]:
  
      APLICAR requer_autenticacao
      APLICAR requer_roles(["PROPRIETARIO"])
      
      SE METODO == POST:
          ATRIBUIR role_alvo = formulario.role // Deve ser ADMINISTRADOR ou PROPRIETARIO
          INSTANCIAR novo_usuario = UsuarioModel(role=role_alvo, criado_por_id=sessao.usuario_id)
          novo_usuario.set_senha(formulario.senha)
          SALVAR_NO_BANCO(novo_usuario)
      
          EXECUTAR registrar_auditoria(sessao.usuario_id, "CRIAR_" + role_alvo, novo_usuario.id)
          RETORNAR REDIRECIONAR("/proprietario/usuarios")
      
      ATRIBUIR lista_usuarios = BUSCAR_USUARIOS_POR_ROLES(["PROPRIETARIO", "ADMINISTRADOR"])
      RETORNAR RENDERIZAR_TEMPLATE("admin/gestao_proprietario.html", usuarios=lista_usuarios)
  
  ROTA "/admin/atendentes" [GET, POST]:
  
      APLICAR requer_autenticacao
      APLICAR requer_roles(["ADMINISTRADOR"]) // Proprietários também podem acessar se desejado na regra de negócio estendida, mas estrito ao ADMIN aqui
      
      SE METODO == POST:
          INSTANCIAR novo_atendente = UsuarioModel(role="ATENDENTE", criado_por_id=sessao.usuario_id)
          novo_atendente.set_senha(formulario.senha)
          SALVAR_NO_BANCO(novo_atendente)
      
          EXECUTAR registrar_auditoria(sessao.usuario_id, "CRIAR_ATENDENTE", novo_atendente.id)
          RETORNAR REDIRECIONAR("/admin/atendentes")
      
      ATRIBUIR lista_atendentes = BUSCAR_USUARIOS_POR_ROLE("ATENDENTE")
      RETORNAR RENDERIZAR_TEMPLATE("admin/gestao_admin.html", atendentes=lista_atendentes)

/app/controllers/ticket_controller.py

- ação: criar

- descrição: Controlador responsável pelo ciclo de vida das solicitações (Tickets).

- pseudocódigo:
  DEFINIR_BLUEPRINT ticket_controller
  IMPORTAR requer_autenticacao, requer_roles DE app.utils.auth_utils
  ROTA "/tickets" [GET]:
  
      APLICAR requer_autenticacao
      SE sessao.usuario_role == "CLIENTE":
          ATRIBUIR tickets = BUSCAR_TICKETS(cliente_id=sessao.usuario_id)
      SE sessao.usuario_role == "ATENDENTE":
          ATRIBUIR tickets = BUSCAR_TODOS_TICKETS()
      RETORNAR RENDERIZAR_TEMPLATE("tickets/lista.html", tickets=tickets)
  
  ROTA "/tickets/novo" [POST]:
  
      APLICAR requer_autenticacao
      APLICAR requer_roles(["CLIENTE"])
      INSTANCIAR novo_ticket = TicketModel(cliente_id=sessao.usuario_id, assunto=formulario.assunto, descricao=formulario.descricao)
      SALVAR_NO_BANCO(novo_ticket)
      RETORNAR REDIRECIONAR("/tickets")
  
  ROTA "/tickets/<int:ticket_id>/responder" [POST]:
  
      APLICAR requer_autenticacao
      APLICAR requer_roles(["ATENDENTE"])
      ATRIBUIR ticket = BUSCAR_TICKET_POR_ID(ticket_id)
      ATUALIZAR ticket.status = formulario.novo_status
      ATUALIZAR ticket.atendente_id = sessao.usuario_id
      // Aqui seria adicionada a lógica textual da resposta se houvesse tabela específica de mensagens
      SALVAR_NO_BANCO(ticket)
      RETORNAR REDIRECIONAR("/tickets")

/app/controllers/relatorio_controller.py

- ação: criar

- descrição: Controlador para geração de relatórios gerenciais para Administradores.

- pseudocódigo:
  DEFINIR_BLUEPRINT relatorio_controller
  IMPORTAR requer_autenticacao, requer_roles DE app.utils.auth_utils
  ROTA "/admin/relatorios" [GET]:
  
      APLICAR requer_autenticacao
      APLICAR requer_roles(["ADMINISTRADOR"])
      
      ATRIBUIR filtro = PARAMETRO_URL("tipo") // Ex: geral, por_atendente, por_admin
      ATRIBUIR dados_relatorio = NULO
      
      SE filtro == "geral":
          dados_relatorio = AGREGAR_TICKETS_TOTAL()
      SE filtro == "por_atendente":
          ATRIBUIR atendente_id = PARAMETRO_URL("atendente_id")
          dados_relatorio = AGREGAR_TICKETS_POR_ATENDENTE(atendente_id)
      SE filtro == "por_admin":
          ATRIBUIR lista_meus_atendentes = BUSCAR_USUARIOS(criado_por_id=sessao.usuario_id)
          dados_relatorio = AGREGAR_TICKETS_POR_LISTA_ATENDENTES(lista_meus_atendentes)
      
      RETORNAR RENDERIZAR_TEMPLATE("admin/relatorios.html", relatorio=dados_relatorio)
