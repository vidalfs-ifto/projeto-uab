import functools
from flask import session, redirect, abort

def requer_autenticacao(funcao_rota):
    @functools.wraps(funcao_rota)
    def wrapper(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect("/login")
        return funcao_rota(*args, **kwargs)
    return wrapper

def requer_roles(lista_roles_permitidas):
    def decorador(funcao_rota):
        @functools.wraps(funcao_rota)
        def wrapper(*args, **kwargs):
            if "usuario_role" not in session or session["usuario_role"] not in lista_roles_permitidas:
                abort(403)
            return funcao_rota(*args, **kwargs)
        return wrapper
    return decorador
