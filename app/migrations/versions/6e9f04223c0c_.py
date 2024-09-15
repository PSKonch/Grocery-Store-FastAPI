"""empty message

Revision ID: 6e9f04223c0c
Revises: f35ae40be905
Create Date: 2024-09-15 13:54:09.520399

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e9f04223c0c'
down_revision: Union[str, None] = 'f35ae40be905'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
