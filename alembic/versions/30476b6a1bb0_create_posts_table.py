"""create posts table

Revision ID: 30476b6a1bb0
Revises: 
Create Date: 2023-08-15 07:18:30.148434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '30476b6a1bb0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # create table
    op.create_table('posts', sa.Column('id', sa.Integer(),
                                       nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
