import enum
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from pydantic import EmailStr

from a8t_tools.db import pagination as pg
from a8t_tools.db import sorting as sr

from app.domain.common.enums import UserStatuses
from app.domain.common.schemas import APIModel


class User(APIModel):
    id: UUID
    firstname: str
    lastname: str
    email: EmailStr
    description: str | None = None
    status: UserStatuses
    created_at: datetime
    code: str | None = None


class UserDetailsFull(User):
    permissions: set[str] | None = None


class UserCredentials(APIModel):
    email: str
    password: str


class UserCredentialsRegist(APIModel):
    firstname: str
    lastname: str
    email: str
    password: str


class UserCredentialsRegistByCode(APIModel):
    firstname: str
    lastname: str
    email: str
    password: str
    code: str


class UserCreate(APIModel):
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr | None = None
    description: str | None = None
    password_hash: str
    permissions: set[str] | None = None


class UserCreateByCode(APIModel):
    firstname: str | None = None
    lastname: str | None = None
    email: EmailStr | None = None
    description: str | None = None
    password_hash: str
    permissions: set[str] | None = None
    code: str


class UserCreateFull(UserCreate):
    status: UserStatuses


class UserPartialUpdate(APIModel):
    firstname: str | None = None
    email: EmailStr | None = None
    permissions: set[str] | None = None
    status: str | None = None


class UserPartialUpdateFull(APIModel):
    password_hash: str | None = None


class UserInternal(APIModel):
    id: UUID
    firstname: str
    lastname: str
    email: EmailStr
    description: str | None = None
    password_hash: str
    permissions: set[str] | None = None
    status: UserStatuses
    created_at: datetime


class UserSorts(enum.StrEnum):
    id = enum.auto()
    firstname = enum.auto()
    email = enum.auto()
    status = enum.auto()
    created_at = enum.auto()


class EmailForCode(APIModel):
    email: str | None = None


class VerificationCode(APIModel):
    code: int


class UpdatePasswordConfirm(APIModel):
    email: str | None = None
    code: str | None = None
    password: str | None = None


class UserProfilePartialUpdate(APIModel):
    firstname: str | None = None
    password: str | None = None


class PasswordResetCode(APIModel):
    user_id: UUID | None = None
    code: str


class EmailVerificationCode(APIModel):
    email: str
    code: int


class PasswordResetCodePartialUpdate(APIModel):
    code: str | None = None


@dataclass
class UserListRequestSchema:
    pagination: pg.PaginationCallable[User] | None = None
    sorting: sr.SortingData[UserSorts] | None = None


@dataclass
class UserWhere:
    id: UUID | None = None
    firstname: str | None = None
    email: str | None = None


@dataclass
class PasswordResetCodeWhere:
    id: int | None = None
    user_id: UUID | None = None
    code: str | None = None