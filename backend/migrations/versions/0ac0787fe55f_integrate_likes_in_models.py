"""integrate likes in models

Revision ID: 0ac0787fe55f
Revises: 96c9052eefbb
Create Date: 2024-04-12 13:35:40.924916

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0ac0787fe55f'
down_revision: Union[str, None] = '96c9052eefbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('likes', sa.Column('content_id', sa.Integer(), nullable=False))
    op.add_column('likes', sa.Column('content_type', sa.Enum('POST', 'COMMENT', 'REPLY', name='contenttypeenum'), nullable=False))
    op.add_column('likes', sa.Column('users_liked', sa.JSON(), nullable=True))
    op.add_column('likes', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('likes', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.create_index(op.f('ix_likes_content_id'), 'likes', ['content_id'], unique=False)
    op.create_index(op.f('ix_likes_content_type'), 'likes', ['content_type'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_likes_content_type'), table_name='likes')
    op.drop_index(op.f('ix_likes_content_id'), table_name='likes')
    op.drop_column('likes', 'updated_at')
    op.drop_column('likes', 'created_at')
    op.drop_column('likes', 'users_liked')
    op.drop_column('likes', 'content_type')
    op.drop_column('likes', 'content_id')
    # ### end Alembic commands ###
