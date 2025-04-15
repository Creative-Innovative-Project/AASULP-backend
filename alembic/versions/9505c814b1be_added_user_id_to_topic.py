"""Added user id to topic

Revision ID: 9505c814b1be
Revises: 56a2b757f26a
Create Date: 2025-04-11 14:14:22.618259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9505c814b1be'
down_revision: Union[str, None] = '56a2b757f26a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
