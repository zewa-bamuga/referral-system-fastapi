from a8t_tools.security.hashing import PasswordHashService

from app.domain.users.core.commands import UserCreateCommand, UserCreateByCodeCommand
from app.domain.users.core.schemas import UserCreate, User, UserCredentialsRegist, UserCredentialsRegistByCode, \
    UserCreateByCode
from app.domain.users.permissions.schemas import BasePermissions


class UserRegisterCommand:
    def __init__(
            self,
            create_command: UserCreateCommand,
            password_hash_service: PasswordHashService,
    ) -> None:
        self.create_command = create_command
        self.password_hash_service = password_hash_service

    async def __call__(self, payload: UserCredentialsRegist) -> User:
        return await self.create_command(
            UserCreate(
                firstname=payload.firstname,
                lastname=payload.lastname,
                email=payload.email,
                password_hash=(await self.password_hash_service.hash(payload.password)),
                avatar_attachment_id=None,
                permissions={BasePermissions.user},
            )
        )


class UserRegisterByCodeCommand:
    def __init__(
            self,
            create_by_code_command: UserCreateByCodeCommand,
            password_hash_service: PasswordHashService,
    ) -> None:
        self.create_by_code_command = create_by_code_command
        self.password_hash_service = password_hash_service

    async def __call__(self, payload: UserCredentialsRegistByCode) -> User:
        return await self.create_by_code_command(
            UserCreateByCode(
                firstname=payload.firstname,
                lastname=payload.lastname,
                email=payload.email,
                password_hash=(await self.password_hash_service.hash(payload.password)),
                avatar_attachment_id=None,
                permissions={BasePermissions.user},
                code=payload.code,
            )
        )
