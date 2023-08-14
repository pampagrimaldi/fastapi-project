"""add content column to posts table

Revision ID: a40f1d9f365b
Revises: 30476b6a1bb0
Create Date: 2023-08-15 07:45:33.826100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a40f1d9f365b'
down_revision: Union[str, None] = '30476b6a1bb0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
