import http

from config import Settings
from fastapi import Depends, HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBase
from telegram_webapp_auth.auth import (
    TelegramAuthenticator,
    TelegramUser,
    generate_secret_key,
)
from telegram_webapp_auth.errors import InvalidInitDataError

telegram_authentication_schema = HTTPBase(scheme="Bearer")


def get_telegram_authenticator() -> TelegramAuthenticator:
    secret_key = generate_secret_key(Settings().token)
    return TelegramAuthenticator(secret_key)


def get_current_user(
    auth_cred: HTTPAuthorizationCredentials = Depends(telegram_authentication_schema),
    telegram_authenticator: TelegramAuthenticator = Depends(get_telegram_authenticator),
) -> TelegramUser:
    try:
        user = telegram_authenticator.verify_token(auth_cred.credentials)
    except InvalidInitDataError:
        raise HTTPException(
            status_code=http.HTTPStatus.FORBIDDEN,
            detail="Forbidden access.",
        ) from InvalidInitDataError
    except Exception:
        raise HTTPException(
            status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Internal error.",
        ) from Exception

    return user
