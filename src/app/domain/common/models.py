import datetime
import secrets
import uuid

import sqlalchemy as sa
from sqlalchemy import orm, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


@orm.as_declarative()
class Base:
    __tablename__: str

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(sa.DateTime(timezone=True), server_default=func.now())
    updated_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class User(Base):
    __tablename__ = "user"

    firstname = Column(String, unique=False, nullable=True)
    lastname = Column(String, unique=False, nullable=True)
    email = Column(String, unique=True, nullable=True)
    description = Column(String, unique=False, nullable=True)
    status = Column(String)
    password_hash = Column(String)
    permissions: orm.Mapped[list[str] | None] = orm.mapped_column(ARRAY(String))

    token = relationship("Token", back_populates="user")
    password_reset_code = relationship("PasswordResetCode", back_populates="user")
    referral_code = relationship("ReferralCode", back_populates="user")
    referrals_made = relationship("Referral", foreign_keys="Referral.referrer_id", back_populates="referrer")
    referrals_received = relationship("Referral", foreign_keys="Referral.referee_id", back_populates="referee")


class Token(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), index=True, nullable=True)
    refresh_token_id = Column(UUID(as_uuid=True))

    user = relationship("User", back_populates="token")


class PasswordResetCode(Base):
    __tablename__ = "password_reset_code"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), index=True, nullable=True)
    code = Column(String, nullable=False)

    user = relationship("User", back_populates="password_reset_code")

    @classmethod
    def generate_code(cls) -> str:
        return secrets.token_urlsafe(6)


class ReferralCode(Base):
    __tablename__ = "referral_code"

    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False, index=True)
    code = Column(String, nullable=False)

    user = relationship("User", back_populates="referral_code")


class Referral(Base):
    __tablename__ = "referral"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    referrer_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False, index=True)
    referee_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete="CASCADE"), nullable=False, index=True)

    referrer = relationship("User", foreign_keys=[referrer_id], back_populates="referrals_made")
    referee = relationship("User", foreign_keys=[referee_id], back_populates="referrals_received")
