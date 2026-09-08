from dataclasses import fields
from typing import Any
from exceptions import CampoAusenteErro


class _FromDictMixin:
    """Mixin que constrói a dataclass a partir de um dict, usando os
    nomes e defaults declarados nos próprios campos da classe.
    """

    @classmethod
    def from_dict(cls, dados: dict[str, Any] | None):
        dados = dados or {}
        kwargs = {
            f.name: dados.get(f.name, f.default)
            for f in fields(cls)
        }
        return cls(**kwargs)


def _navegar_json(data: dict, chaves: tuple):
    """Navega por níveis de um dicionário passando as chaves em sequência."""
    atual = data
    caminho_percorrido = []

    for chave in chaves:
        caminho_percorrido.append(chave)

        if not isinstance(atual, dict) or chave not in atual:
            raise CampoAusenteErro(f"Chave '{chave}' ausente no JSON!")

        atual = atual[chave]

    return atual
