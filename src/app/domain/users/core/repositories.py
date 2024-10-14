from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.sql.elements import ColumnElement
import sqlalchemy as sa

from a8t_tools.db.pagination import PaginationCallable, Paginated
from a8t_tools.db.sorting import SortingData
from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.db.utils import CrudRepositoryMixin

from app.domain.common import models, enums
from app.domain.common.schemas import IdContainer
from app.domain.users.code import schemas as codeschema
from app.domain.users.core import schemas


class ReferralCodeRpository(CrudRepositoryMixin[models.ReferralCode]):
    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.ReferralCode
        self.transaction = transaction

    async def create_code(self, payload: codeschema.ReferralCodeCreate) -> IdContainer:
        return IdContainer(id=await self._create(payload))

    async def get_code_by_filter_or_none(self, where: codeschema.CodeWhere) -> codeschema.CodeInternal | None:
        return await self._get_or_none(
            codeschema.CodeInternal,
            condition=await self._format_filters(where),
        )

    async def _format_filters(self, where: codeschema.CodeWhere) -> ColumnElement[bool]:
        filters: list[ColumnElement[bool]] = []

        if where.id is not None:
            filters.append(models.ReferralCode.id == where.id)

        if where.user_id is not None:
            filters.append(models.ReferralCode.user_id == where.user_id)

        if where.code is not None:
            filters.append(models.ReferralCode.code == where.code)

        return and_(*filters)

    async def code_deletion(self, user_id: UUID) -> None:
        async with self.transaction.use() as session:
            check_query = select(models.ReferralCode).where(models.ReferralCode.user_id == user_id)
            result = await session.execute(check_query)
            code_exists = result.first()

            if code_exists:
                stmt = sa.delete(models.ReferralCode).where(models.ReferralCode.user_id == user_id)
                await session.execute(stmt)
                await session.commit()


class ReferralRpository(CrudRepositoryMixin[models.Referral]):
    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.Referral
        self.transaction = transaction

    async def create_referee(self, payload: codeschema.RefereeCreate) -> IdContainer:
        return IdContainer(id=await self._create(payload))

    async def get_referee_by_filter_or_none(self, where: codeschema.RefereeWhere) -> codeschema.RefereeInternal | None:
        return await self._get_or_none(
            codeschema.RefereeInternal,
            condition=await self._format_filters(where),
        )

    async def _format_filters(self, where: codeschema.RefereeWhere) -> ColumnElement[bool]:
        filters: list[ColumnElement[bool]] = []

        print("Реферал: ", where.referrer_id)
        print("Реферал: ", where.referee_id)

        if where.id is not None:
            filters.append(models.Referral.id == where.id)

        if where.referrer_id is not None:
            filters.append(models.Referral.referrer_id == where.referrer_id)

        if where.referee_id is not None:
            filters.append(models.Referral.referee_id == where.referee_id)

        return and_(*filters)


class UserRepository(CrudRepositoryMixin[models.User]):
    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.User
        self.transaction = transaction

    async def get_users(
            self,
            pagination: PaginationCallable[schemas.User] | None = None,
            sorting: SortingData[schemas.UserSorts] | None = None,
    ) -> Paginated[schemas.User]:
        return await self._get_list(
            schemas.User,
            pagination=pagination,
            sorting=sorting,
        )

    async def get_user_by_filter_or_none(self, where: schemas.UserWhere) -> schemas.UserInternal | None:
        return await self._get_or_none(
            schemas.UserInternal,
            condition=await self._format_filters(where),
        )

    async def get_user_by_filter_by_email_or_none(self, where: schemas.UserWhere) -> schemas.UserInternal | None:
        return await self._get_or_none(
            schemas.UserInternal,
            condition=await self._format_filters_email(where),
        )

    async def create_user(self, payload: schemas.UserCreate) -> IdContainer:
        return IdContainer(id=await self._create(payload))

    async def partial_update_user(self, user_id: UUID, payload: schemas.UserPartialUpdate) -> None:
        return await self._partial_update(user_id, payload)

    async def delete_user(self, user_id: UUID) -> None:
        return await self._delete(user_id)

    async def set_user_status(self, user_id: UUID, status: enums.UserStatuses) -> None:
        return await self._partial_update(user_id, schemas.UserPartialUpdate(status=status))

    async def get_password_reset_code_by_code_or_none(self,
                                                      where: schemas.PasswordResetCodeWhere) -> schemas.PasswordResetCode | None:
        return await self._get_or_none(
            schemas.PasswordResetCode,
            condition=await self._format_filters_code(where),
        )

    async def _format_filters(self, where: schemas.UserWhere) -> ColumnElement[bool]:
        filters: list[ColumnElement[bool]] = []

        if where.id is not None:
            filters.append(models.User.id == where.id)

        if where.firstname is not None:
            filters.append(models.User.firstname == where.firstname)

        return and_(*filters)

    async def _format_filters_email(self, where: schemas.UserWhere) -> ColumnElement[bool]:
        filters: list[ColumnElement[bool]] = []

        if where.id is not None:
            filters.append(models.User.id == where.id)

        if where.email is not None:
            filters.append(models.User.email == where.email)

        return and_(*filters)
