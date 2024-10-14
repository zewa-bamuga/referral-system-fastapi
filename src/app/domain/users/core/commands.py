from uuid import UUID

from a8t_tools.bus.producer import TaskProducer
from fastapi import HTTPException
from loguru import logger

from app.domain.common import enums
from app.domain.common.exceptions import NotFoundError
from app.domain.common.schemas import IdContainer
from app.domain.users.core import schemas
from app.domain.users.code import schemas as codeschema
from app.domain.users.core.repositories import UserRepository, ReferralCodeRpository, ReferralRpository


class UserPartialUpdateCommand:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, user_id: UUID, payload: schemas.UserPartialUpdate) -> schemas.UserDetailsFull:
        try:
            await self.user_repository.partial_update_user(user_id, payload)
            user = await self.user_repository.get_user_by_filter_or_none(schemas.UserWhere(id=user_id))

            if not user:
                raise NotFoundError()

        except Exception as e:
            print("Произошла ошибка при обновлении пользователя или сотрудника:", e)
            raise

        return schemas.UserDetailsFull.model_validate(user)


class UserCreateCommand:
    def __init__(
            self,
            user_repository: UserRepository,
            task_producer: TaskProducer,
    ):
        self.user_repository = user_repository
        self.task_producer = task_producer

    async def __call__(self, payload: schemas.UserCreate) -> schemas.User:
        user_id_container = await self.user_repository.create_user(
            schemas.UserCreateFull(
                status=enums.UserStatuses.unconfirmed,
                **payload.model_dump(),
            )
        )
        logger.info(f"User created: {user_id_container.id}")
        await self._enqueue_user_activation(user_id_container)
        user = await self.user_repository.get_user_by_filter_or_none(schemas.UserWhere(id=user_id_container.id))
        assert user

        return schemas.User.model_validate(user)

    async def _enqueue_user_activation(self, user_id_container: IdContainer) -> None:
        await self.task_producer.fire_task(
            enums.TaskNames.activate_user,
            queue=enums.TaskQueues.main_queue,
            user_id_container_dict=user_id_container.json_dict(),
        )


class UserCreateByCodeCommand:
    def __init__(
            self,
            user_repository: UserRepository,
            task_producer: TaskProducer,
            referral_code_repository: ReferralCodeRpository,
            referral_repository: ReferralRpository,
    ):
        self.user_repository = user_repository
        self.task_producer = task_producer
        self.referral_code_repository = referral_code_repository
        self.referral_repository = referral_repository

    async def __call__(self, payload: schemas.UserCreateByCode) -> schemas.User:
        if not payload.code:
            raise HTTPException(status_code=400, detail="Referral code is required for registration")

        referrer_id = await self.referral_code_repository.get_code_by_filter_or_none(
            codeschema.CodeWhere(code=payload.code))

        if not referrer_id:
            raise HTTPException(status_code=400, detail="Invalid referral code")

        user_id_container = await self.user_repository.create_user(
            schemas.UserCreateFull(
                status=enums.UserStatuses.unconfirmed,
                **payload.model_dump(),
            )
        )
        logger.info(f"User created: {user_id_container.id}")
        await self._enqueue_user_activation(user_id_container)

        user = await self.user_repository.get_user_by_filter_or_none(schemas.UserWhere(id=user_id_container.id))
        assert user

        await self.referral_repository.create_referee(
            codeschema.RefereeCreate(
                referrer_id=referrer_id.user_id,
                referee_id=user_id_container.id,
            )
        )

        return schemas.User.model_validate(user)

    async def _enqueue_user_activation(self, user_id_container: IdContainer) -> None:
        await self.task_producer.fire_task(
            enums.TaskNames.activate_user,
            queue=enums.TaskQueues.main_queue,
            user_id_container_dict=user_id_container.json_dict(),
        )


class UserActivateCommand:
    def __init__(
            self,
            repository: UserRepository,
    ):
        self.repository = repository

    async def __call__(self, user_id: UUID) -> None:
        await self.repository.set_user_status(user_id, enums.UserStatuses.active)
