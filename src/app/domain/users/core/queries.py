from uuid import UUID

from a8t_tools.db.pagination import Paginated

from app.domain.common.exceptions import NotFoundError
from app.domain.users.core import schemas
from app.domain.users.core.repositories import UserRepository


class EmailRetrieveQuery:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def __call__(self, user_email: str) -> schemas.UserInternal:
        result = await self.repository.get_user_by_filter_by_email_or_none((schemas.UserWhere(email=user_email)))
        if not result:
            raise NotFoundError()
        return schemas.UserInternal.model_validate(result)


class UserRetrieveByUsernameQuery:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def __call__(self, firstname: str) -> schemas.UserInternal | None:
        return await self.repository.get_user_by_filter_or_none(schemas.UserWhere(firstname=firstname))


class UserRetrieveByEmailQuery:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, email: str) -> schemas.UserInternal | None:
        try:
            user_internal = await self.user_repository.get_user_by_filter_by_email_or_none(
                schemas.UserWhere(email=email))
        except Exception as e:
            print("не попал:", e)
            user_internal = None

        return user_internal


class UserRetrieveQuery:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, user_id: UUID) -> schemas.UserInternal:
        result = await self.user_repository.get_user_by_filter_or_none(schemas.UserWhere(id=user_id))
        if not result:
            raise NotFoundError()
        return schemas.UserInternal.model_validate(result)


class UserListQuery:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def __call__(self, payload: schemas.UserListRequestSchema) -> Paginated[schemas.User]:
        return await self.repository.get_users(payload.pagination, payload.sorting)
