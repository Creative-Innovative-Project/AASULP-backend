"""Corrected error

Revision ID: e00647385def
Revises: 12ec5cb74855
Create Date: 2025-04-11 17:44:41.756358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e00647385def'
down_revision: Union[str, None] = '12ec5cb74855'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
