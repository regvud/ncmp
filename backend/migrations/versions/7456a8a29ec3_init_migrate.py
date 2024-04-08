"""init migrate

Revision ID: 7456a8a29ec3
Revises: 
Create Date: 2024-04-08 12:11:43.724827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7456a8a29ec3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_profile_avatars_profile_id'), 'profile_avatars', ['profile_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_profile_avatars_profile_id'), table_name='profile_avatars')
    # ### end Alembic commands ###