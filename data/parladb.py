import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from tinydb import Query, TinyDB


@dataclass
class Registrador:
    nomeuser: str # Por qual nome deseja ser chamado
    nometelegram: str # Nome de usuário no telegram
    data: str # Data em que foi realizado o registro
    rep_dep: str # Se acessor, representa qual deputado
    tipo: Literal['acessor', 'deputado'] = 'deputado' # Classificação

    def as_dict(self):
        return asdict(self)

def inserir_dado(usuario, usertele, data, types):

    db_path = Path(__file__).parent / 'deputados.db'

    r1 = Registrador(usuario, usertele, data, types)

    db = TinyDB(db_path, indent=4)
    index1 = db.insert(r1.as_dict())

    return index1

def todo_banco():
    db_path = Path(__file__).parent / 'deputados.db'
    db = TinyDB(db_path, indent=4)
    return db.all()

def remover_elm(nomeuser):
    Loc = Query()
    db_path = Path(__file__).parent / 'deputados.db'
    db = TinyDB(db_path, indent=4)
    return(db.remove(Loc.nometelegram == nomeuser))


def limpar_banco():
    db_path = Path(__file__).parent / 'deputados.db'
    db = TinyDB(db_path, indent=4)
    db.truncate()

def buscar_pnome(nomeuser):
    Loc = Query()
    db_path = Path(__file__).parent / 'deputados.db'
    db = TinyDB(db_path, indent=4)
    return db.get(Loc.nometelegram == nomeuser)

if __name__ == '__main__':
    limpar_banco()