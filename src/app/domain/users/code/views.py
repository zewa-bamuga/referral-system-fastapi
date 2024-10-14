from contextlib import asynccontextmanager
from uuid import UUID

from a8t_tools.security.tokens import override_user_token
from dependency_injector import wiring
from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends, Header
from starlette import status

from app.containers import Container
from app.domain.users.code.commands import CreateReferralCodeCommand, DeleteReferralCodeCommand, SendReferralCodeCommand
from app.domain.users.code.queries import ReferralQuery
from app.domain.users.code.schemas import CodeInternal, SendCode
from app.domain.users.core.schemas import User


router = APIRouter()


@asynccontextmanager
async def user_token(token: str):
    async with override_user_token(token or ""):
        yield


@router.post(
    "/create",
    response_model=CodeInternal,
)
@wiring.inject
async def referral_code_create(
        token: str = Header(...),
        command: CreateReferralCodeCommand = Depends(wiring.Provide[Container.user.create_referral_code_command]),
):
    async with user_token(token):
        return await command()


@router.delete(
    "/delete",
    status_code=status.HTTP_204_NO_CONTENT,
)
@wiring.inject
async def referral_code_delete(
        token: str = Header(...),
        command: DeleteReferralCodeCommand = Depends(wiring.Provide[Container.user.delete_referral_code_command]),
) -> None:
    async with user_token(token):
        return await command()


@router.post(
    "/send",
    status_code=status.HTTP_204_NO_CONTENT,
)
@wiring.inject
async def send_code(
        payload: SendCode,
        token: str = Header(...),
        command: SendReferralCodeCommand = Depends(wiring.Provide[Container.user.send_referral_code_command]),
) -> None:
    async with user_token(token):
        return await command(payload)


@router.get(
    "/get/info/referral",
    response_model=User,
)
@wiring.inject
async def get_information(
        referee_id: UUID,
        token: str = Header(...),
        query: ReferralQuery = Depends(Provide[Container.user.referral_query]),
) -> User:
    async with user_token(token):
        return await query(referee_id)