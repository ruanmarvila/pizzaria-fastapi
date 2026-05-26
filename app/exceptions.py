class ModelError(Exception):
    def __init__(self, mensagem: str):
        self.mensagem = mensagem

class TokenInvalidoError(ModelError):
    def __init__(self, mensagem="Token Inválido"):
        super().__init__(mensagem)

class TokenExpiradoError(ModelError):
    def __init__(self, mensagem="Token Expirado"):
        super().__init__(mensagem)

class CredenciaisInvalidasError(ModelError):
    def __init__(self, mensagem="Email ou senha inválidos"):
        super().__init__(mensagem)

class AcessoNegadoError(ModelError):
    def __init__(self, mensagem="Acesso Negado"):
        super().__init__(mensagem)

class UsuarioDesativadoError(ModelError):
    def __init__(self, mensagem="Usuário Desativado ou Excluído"):
        super().__init__(mensagem)

class PedidoNaoEncontradoError(ModelError):
    def __init__(self, mensagem="Pedido não encontrado"):
        super().__init__(mensagem)

class UsuarioNaoEncontradoError(ModelError):
    def __init__(self, mensagem="Usuário não encontrado"):
        super().__init__(mensagem)

class EmailJaCadastradoError(ModelError):
    def __init__(self, mensagem="Já existe um usuário com esse email"):
        super().__init__(mensagem)

class ContaAtivaError(ModelError):
    def __init__(self, mensagem="A conta já está ativa"):
        super().__init__(mensagem)

class AtualizarStatusPedidoError(ModelError):
    def __init__(self, mensagem="Erro ao atualizar o status do pedido"):
        super().__init__(mensagem)

class RecuperacaoContaExpiradoError(ModelError):
    def __init__(self, mensagem="O prazo de 30 dias pra recuperar sua conta expirou"):
        super().__init__(mensagem)

