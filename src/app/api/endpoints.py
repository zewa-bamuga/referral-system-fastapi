from fastapi import APIRouter, status

import app.domain.users.auth.views
import app.domain.users.registration.views
import app.domain.users.code.views
from app.api import schemas

auth = APIRouter(prefix="/authentication")
auth.include_router(
    app.domain.users.registration.views.router,
    prefix="/v1",
    tags=["Authentication"]
)
auth.include_router(
    app.domain.users.auth.views.router,
    prefix="/v1",
    tags=["Authentication"]
)

code = APIRouter(prefix="/referral-code")
code.include_router(
    app.domain.users.code.views.router,
    prefix="/v1",
    tags=["Referral Code"]
)

router = APIRouter(
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": schemas.AuthApiError},
        status.HTTP_403_FORBIDDEN: {"model": schemas.SimpleApiError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.SimpleApiError},
    }
)

router.include_router(auth)
router.include_router(code)
