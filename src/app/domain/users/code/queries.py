from uuid import UUID

from app.domain.users.auth.queries import CurrentUserQuery
from app.domain.users.code import schemas as code_schemas
from app.domain.users.core import schemas
from app.domain.users.core.repositories import ReferralRpository, UserRepository
from app.domain.users.core.schemas import User
from app.domain.users.profile.queries import UserProfileMeQuery


class ReferralQuery:
    def __init__(
            self,
            current_user_query: CurrentUserQuery,
            profile_me_query: UserProfileMeQuery,
            referral_repository: ReferralRpository,
            user_repository: UserRepository,
    ) -> None:
        self.current_user_query = current_user_query
        self.profile_me_query = profile_me_query
        self.referral_repository = referral_repository
        self.user_repository = user_repository

    async def __call__(self, referee_id: UUID) -> User:
        print("user_id", referee_id)
        referrer = await self.current_user_query()

        referee = await self.referral_repository.get_referee_by_filter_or_none(
            code_schemas.RefereeWhere(referrer_id=referrer.id, referee_id=referee_id))

        print("referee_id", referee.referee_id)

        result = await self.user_repository.get_user_by_filter_or_none(schemas.UserWhere(id=referee.referee_id))

        print("referee", referee)

        return schemas.User.model_validate(result)
