"""Exceções compartilhadas entre os módulos."""


class RegistroDuplicadoErro(Exception):
    """Lançada quando um valor que deve ser único já existe no banco."""

    def __init__(self, campo: str):
        super().__init__(campo)
        self.campo = campo


class RegistroNaoEncontradoErro(Exception):
    """Lançada quando o registro pedido não existe."""
