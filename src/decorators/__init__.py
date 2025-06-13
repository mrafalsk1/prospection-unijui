from functools import wraps
from flask_restx import Namespace
from flask import request, current_app
from flask_restx.api import HTTPStatus

from ..utils.service_utils import ServiceResult, ServiceError


def handle_service_result(ns: Namespace):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            result: ServiceResult = fn(*args, **kwargs)

            if not result.success:
                error_type = result.error_type
                message = result.message

                if error_type == ServiceError.NOT_FOUND:
                    ns.abort(404, message)
                elif error_type == ServiceError.ALREADY_EXISTS:
                    ns.abort(409, message)
                elif error_type == ServiceError.INVALID_INPUT:
                    ns.abort(400, message)
                elif error_type == ServiceError.DEPENDENCY_ERROR:
                    ns.abort(400, message)
                else:
                    ns.abort(500, message)

            if result.data is None and result.success:
                return "", 204

            return result.data

        wrapper.__name__ = fn.__name__
        return wrapper

    return decorator


def auth(ns):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            api_key = current_app.config.get("SECRET_KEY")
            if not api_key:
                ns.abort(
                    HTTPStatus(500), "A chave de API não foi configurada no servidor."
                )
                return

            auth_header = request.headers.get("Authorization")
            if not auth_header:
                ns.abort(HTTPStatus(401), "O cabeçalho de autorização é obrigatório.")
                return

            provided_key = None
            try:
                auth_type, provided_key = auth_header.split()
                if auth_type.lower() != "apikey":
                    ns.abort(
                        HTTPStatus(401), 'Tipo de autorização inválido. Use "ApiKey".'
                    )
                    return
                if not provided_key:
                    ns.abort(
                        HTTPStatus(401), 'Tipo de autorização inválido. Use "ApiKey".'
                    )
                    return
            except ValueError:
                ns.abort(
                    HTTPStatus(401),
                    'Formato do cabeçalho de autorização inválido. Use "ApiKey <token>".',
                )

            if provided_key != api_key:
                ns.abort(HTTPStatus(401), "Chave de API inválida ou incorreta.")
                return

            return fn(*args, **kwargs)

        wrapper.__name__ = fn.__name__
        return wrapper

    return decorator
