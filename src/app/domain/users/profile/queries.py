from app.domain.users.auth.queries import CurrentUserQuery
from app.domain.users.core.schemas import User


class UserProfileMeQuery:
    def __init__(
            self,
            current_user_query: CurrentUserQuery,
    ) -> None:
        self.current_user_query = current_user_query

    async def __call__(self) -> User:
        return await self.current_user_query()
