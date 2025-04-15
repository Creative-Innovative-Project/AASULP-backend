"""Corrected error

Revision ID: 12ec5cb74855
Revises: 3a3799d7b227
Create Date: 2025-04-11 17:44:15.231109

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12ec5cb74855'
down_revision: Union[str, None] = '3a3799d7b227'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
