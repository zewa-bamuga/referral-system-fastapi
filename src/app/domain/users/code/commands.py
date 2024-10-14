import uuid
import datetime
from loguru import logger

from app.domain.users.auth.queries import CurrentUserQuery
from app.domain.users.code import schemas
from app.domain.users.core.email import ReferralCodeSender
from app.domain.users.core.repositories import ReferralCodeRpository


class ReferralCode:
    def __init__(self, valid_duration_minutes: int):
        self.code = self._generate_code()
        self.created_at = datetime.datetime.utcnow()
        self.valid_duration = datetime.timedelta(minutes=valid_duration_minutes)
        self.expires_at = self.created_at + self.valid_duration

    def _generate_code(self) -> str:
        """Генерация уникального реферального кода."""
        return str(uuid.uuid4())

    def is_valid(self) -> bool:
        """Проверка, действителен ли код."""
        now = datetime.datetime.utcnow()
        return now < self.expires_at

    def get_time_remaining(self) -> str:
        """Получение оставшегося времени действия кода."""
        now = datetime.datetime.utcnow()
        if now > self.expires_at:
            return "Code has expired"
        time_remaining = self.expires_at - now
        return str(time_remaining)


class CreateReferralCodeCommand:
    def __init__(
            self,
            referral_code_repository: ReferralCodeRpository,
            create_referral_code: ReferralCode,
            current_user_query: CurrentUserQuery,
    ) -> None:
        self.create_referral_code = create_referral_code
        self.current_user_query = current_user_query
        self.referral_code_repository = referral_code_repository

    async def __call__(self) -> schemas.ReferralCodeCreate:
        create_referral_code = ReferralCode(valid_duration_minutes=60)

        current_user = await self.current_user_query()
        user_id = current_user.id

        await self.referral_code_repository.code_deletion(user_id)

        referral_code_id_container = await self.referral_code_repository.create_code(
            schemas.ReferralCodeCreate(
                user_id=user_id,
                code=create_referral_code.code,
            )
        )
        logger.info(f"Referral code: {referral_code_id_container.id}")

        referral_code = await self.referral_code_repository.get_code_by_filter_or_none(
            schemas.CodeWhere(user_id=user_id))

        return schemas.CodeInternal.model_validate(referral_code)


class DeleteReferralCodeCommand:
    def __init__(
            self,
            referral_code_repository: ReferralCodeRpository,
            current_user_query: CurrentUserQuery,
    ) -> None:
        self.current_user_query = current_user_query
        self.referral_code_repository = referral_code_repository

    async def __call__(self) -> None:
        current_user = await self.current_user_query()
        user_id = current_user.id

        await self.referral_code_repository.code_deletion(user_id)


class SendReferralCodeCommand:
    def __init__(
            self,
            referral_code_repository: ReferralCodeRpository,
            current_user_query: CurrentUserQuery,
            send_email: ReferralCodeSender,
    ) -> None:
        self.current_user_query = current_user_query
        self.referral_code_repository = referral_code_repository
        self.send_email = send_email

    async def __call__(self, payload: schemas.SendCode) -> None:
        current_user = await self.current_user_query()
        user_id = current_user.id

        referral_code = await self.referral_code_repository.get_code_by_filter_or_none(
            schemas.CodeWhere(user_id=user_id))

        await self.send_email.send_referral_code(email=payload.email, code=referral_code.code)
