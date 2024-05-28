"""added user_like model

Revision ID: 8ca24135cbd2
Revises: 755369480253
Create Date: 2024-04-12 14:18:23.617399

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8ca24135cbd2'
down_revision: Union[str, None] = '755369480253'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_likes_count', table_name='likes')
    op.drop_column('likes', 'users_liked')
    op.drop_column('likes', 'count')
    op.add_column('user_like', sa.Column('user_id', sa.Integer(), nullable=True))
    op.add_column('user_like', sa.Column('like_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_user_like_like_id'), 'user_like', ['like_id'], unique=False)
    op.create_index(op.f('ix_user_like_user_id'), 'user_like', ['user_id'], unique=False)
    op.create_foreign_key(None, 'user_like', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'user_like', 'likes', ['like_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_like', type_='foreignkey')
    op.drop_constraint(None, 'user_like', type_='foreignkey')
    op.drop_index(op.f('ix_user_like_user_id'), table_name='user_like')
    op.drop_index(op.f('ix_user_like_like_id'), table_name='user_like')
    op.drop_column('user_like', 'like_id')
    op.drop_column('user_like', 'user_id')
    op.add_column('likes', sa.Column('count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('likes', sa.Column('users_liked', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.create_index('ix_likes_count', 'likes', ['count'], unique=False)
    # ### end Alembic commands ###
