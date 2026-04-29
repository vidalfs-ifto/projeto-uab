# Plano de Testes - Sistema de Atendimento (TDD First)

Este documento descreve a estratégia de testes automatizados para o Sistema de Atendimento, seguindo a metodologia TDD (Test-Driven Development). O foco principal é garantir a integridade das regras de negócio, segurança (autorização por roles) e estabilidade do sistema.

## 1. Objetivos
- Validar as funcionalidades críticas descritas em `doc/03-especs.md`.
- Garantir que as restrições de acesso (roles) sejam rigorosamente respeitadas.
- Assegurar a persistência correta de dados e logs de auditoria.
- Prevenir regressões durante o ciclo de desenvolvimento.

## 2. Ambiente de Testes e Dependências

### Ferramentas
- **Framework:** `pytest`
- **Integração Flask:** `pytest-flask`
- **Mocks:** `pytest-mock`
- **Cobertura:** `pytest-cov`
- **Banco de Dados:** SQLite em memória (para isolamento e performance).

### Execução dos Testes
```bash
# Executar todos os testes
pytest

# Executar com relatório de cobertura
pytest --cov=app tests/
```

## 3. Estratégia de Teste

### 3.1. Testes de Unidade (Models e Utils)
Foco na lógica interna das classes e funções auxiliares.
- **UsuarioModel:** Validação de hash de senha.
- **AuthUtils:** Verificação dos decoradores `requer_autenticacao` e `requer_roles`.
- **LogUtils:** Garantia de que a função de auditoria cria os registros corretamente.

### 3.2. Testes de Integração (Controllers/Endpoints)
Simulação de requisições HTTP para validar o fluxo completo (Request -> Controller -> Model -> Response).
- Fluxo de login e sessão.
- CRUD de usuários com diferentes privilégios.
- Ciclo de vida de tickets.

### 3.3. Uso de Mocks
- **OAuth Google:** Simulação da resposta do provedor externo (Authlib/Google API).
- **Email (se aplicável):** Mock de envio de notificações.

## 4. Plano de Casos de Teste por Funcionalidade

### 4.1. Autenticação e Autorização (Crítico)
| Caso de Teste | Descrição | Prioridade |
| :--- | :--- | :--- |
| CT-01: Login Sucesso | Validar login com credenciais válidas e criação de sessão. | Alta |
| CT-02: Login Falha | Tentar login com senha incorreta ou usuário inexistente. | Alta |
| CT-03: Acesso Negado | Tentar acessar rota de ADMIN com role de CLIENTE (403). | Alta |
| CT-04: Mock OAuth | Simular callback do Google com sucesso e criação de usuário CLIENTE. | Média |

### 4.2. Gestão de Usuários e Auditoria
| Caso de Teste | Descrição | Prioridade |
| :--- | :--- | :--- |
| CT-05: Criar Admin | PROPRIETARIO criando ADMINISTRADOR e verificando log de auditoria. | Alta |
| CT-06: Criar Atendente | ADMINISTRADOR criando ATENDENTE e verificando log. | Alta |
| CT-07: Bloqueio Hierárquico | Tentar criar PROPRIETARIO usando conta de ADMINISTRADOR (deve falhar). | Crítica |

### 4.3. Fluxo de Tickets
| Caso de Teste | Descrição | Prioridade |
| :--- | :--- | :--- |
| CT-08: Abertura Ticket | CLIENTE cria novo ticket e verifica status "ABERTO". | Alta |
| CT-09: Resposta Ticket | ATENDENTE assume ticket, muda status para "EM_ANDAMENTO" e salva. | Alta |
| CT-10: Visibilidade | CLIENTE só pode ver seus próprios tickets; ATENDENTE vê todos. | Crítica |

### 4.4. Relatórios Gerenciais
| Caso de Teste | Descrição | Prioridade |
| :--- | :--- | :--- |
| CT-11: Filtro Relatório | ADMIN acessa relatórios agregados por atendente. | Média |

## 5. Mocking e Fixtures (Exemplos Técnicos)

Para implementar o TDD, utilizaremos fixtures do pytest para preparar o estado do banco:

```python
@pytest.fixture
def app():
    app = create_app()
    app.config.update({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
```

## 6. Próximos Passos (TDD Workflow)
1. Criar o arquivo de teste (ex: `tests/test_auth.py`).
2. Definir o teste que falha (Red).
3. Implementar o código mínimo necessário no Controller/Model.
4. Validar o teste (Green).
5. Refatorar se necessário.
