"""Corrected error

Revision ID: 3a3799d7b227
Revises: 442fba7a6c2a
Create Date: 2025-04-11 17:43:23.966970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a3799d7b227'
down_revision: Union[str, None] = '442fba7a6c2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
