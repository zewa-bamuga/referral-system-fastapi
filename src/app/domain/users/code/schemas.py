from dataclasses import dataclass

from a8t_tools.schemas.pydantic import APIModel
from uuid import UUID


class ReferralCode(APIModel):
    code: str


class ReferralCodeCreate(APIModel):
    user_id: UUID
    code: str


class RefereeCreate(APIModel):
    referrer_id: UUID
    referee_id: UUID


class CodeInternal(APIModel):
    id: UUID | None = None
    user_id: UUID
    code: str


class RefereeInternal(APIModel):
    id: UUID | None = None
    referrer_id: UUID
    referee_id: UUID


class SendCode(APIModel):
    email: str
    code: str


@dataclass
class CodeWhere:
    id: UUID | None = None
    user_id: UUID | None = None
    code: str | None = None


@dataclass
class RefereeWhere:
    id: UUID | None = None
    referrer_id: UUID | None = None
    referee_id: UUID | None = None
