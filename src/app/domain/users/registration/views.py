from dependency_injector import wiring
from fastapi import APIRouter, Depends

from app.containers import Container
from app.domain.users.core.schemas import User, UserCredentialsRegist, UserCredentialsRegistByCode
from app.domain.users.registration.commands import UserRegisterCommand, UserRegisterByCodeCommand
from app.domain.users.registration.hi import send_hello

router = APIRouter()


@router.post(
    "/registration",
    response_model=User,
)
@wiring.inject
async def register(
        payload: UserCredentialsRegist,
        command: UserRegisterCommand = Depends(wiring.Provide[Container.user.register_command]),
) -> User:
    user_details = await command(payload)
    await send_hello(user_details)
    return user_details


@router.post(
    "/registration/by/code",
    response_model=User,
)
@wiring.inject
async def register_by_code(
        payload: UserCredentialsRegistByCode,
        command: UserRegisterByCodeCommand = Depends(wiring.Provide[Container.user.register_by_code_command]),
) -> User:
    user_details = await command(payload)
    await send_hello(user_details)
    return user_details
