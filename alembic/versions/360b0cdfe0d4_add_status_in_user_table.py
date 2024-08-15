"""add status in user table

Revision ID: 360b0cdfe0d4
Revises: 2333d84e30f8
Create Date: 2024-08-15 09:37:51.205686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '360b0cdfe0d4'
down_revision: Union[str, None] = '2333d84e30f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('status', sa.Boolean))


def downgrade() -> None:
    op.drop_column('users', 'status')
