from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions import ModelError, TokenInvalidoError ,TokenExpiradoError, CredenciaisInvalidasError,AcessoNegadoError, PedidoNaoEncontradoError, UsuarioNaoEncontradoError, EmailJaCadastradoError
from app.routers import admin_router, auth_router, order_router

app = FastAPI()

MAPA_ERROR_HTTP = {
    TokenInvalidoError: status.HTTP_401_UNAUTHORIZED,
    TokenExpiradoError: status.HTTP_401_UNAUTHORIZED,
    CredenciaisInvalidasError: status.HTTP_401_UNAUTHORIZED,
    AcessoNegadoError: status.HTTP_403_FORBIDDEN,
    PedidoNaoEncontradoError: status.HTTP_404_NOT_FOUND,
    UsuarioNaoEncontradoError: status.HTTP_404_NOT_FOUND,
    EmailJaCadastradoError: status.HTTP_409_CONFLICT
}

@app.exception_handler(ModelError)
async def model_error_handler(request: Request, exc: ModelError) -> JSONResponse:
    status_code = MAPA_ERROR_HTTP.get(type(exc), status.HTTP_400_BAD_REQUEST)

    return JSONResponse(
        status_code= status_code,
        content={"detail": exc.mensagem}
    )

app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(order_router)

# uvicorn app.main:app --reload

#TODO