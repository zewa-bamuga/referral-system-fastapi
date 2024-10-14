"""empty message

Revision ID: ff5e7353be58
Revises: 
Create Date: 2024-10-13 16:53:24.619080

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ff5e7353be58'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('firstname', sa.String(), nullable=True),
    sa.Column('lastname', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.Column('permissions', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('password_reset_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_password_reset_code_user_id'), 'password_reset_code', ['user_id'], unique=False)
    op.create_table('referral',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('referrer_id', sa.UUID(), nullable=False),
    sa.Column('referee_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['referee_id'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['referrer_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_referral_id'), 'referral', ['id'], unique=False)
    op.create_index(op.f('ix_referral_referee_id'), 'referral', ['referee_id'], unique=False)
    op.create_index(op.f('ix_referral_referrer_id'), 'referral', ['referrer_id'], unique=False)
    op.create_table('referral_code',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_referral_code_id'), 'referral_code', ['id'], unique=False)
    op.create_index(op.f('ix_referral_code_user_id'), 'referral_code', ['user_id'], unique=False)
    op.create_table('token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('refresh_token_id', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_token_user_id'), 'token', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_token_user_id'), table_name='token')
    op.drop_table('token')
    op.drop_index(op.f('ix_referral_code_user_id'), table_name='referral_code')
    op.drop_index(op.f('ix_referral_code_id'), table_name='referral_code')
    op.drop_table('referral_code')
    op.drop_index(op.f('ix_referral_referrer_id'), table_name='referral')
    op.drop_index(op.f('ix_referral_referee_id'), table_name='referral')
    op.drop_index(op.f('ix_referral_id'), table_name='referral')
    op.drop_table('referral')
    op.drop_index(op.f('ix_password_reset_code_user_id'), table_name='password_reset_code')
    op.drop_table('password_reset_code')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
