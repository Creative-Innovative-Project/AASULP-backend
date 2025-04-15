"""Added week_id to quiz table

Revision ID: 5e11d3f71a17
Revises: 9505c814b1be
Create Date: 2025-04-11 17:37:27.261256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e11d3f71a17'
down_revision: Union[str, None] = '9505c814b1be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
