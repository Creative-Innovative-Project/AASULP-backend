"""Changed foreign key for week

Revision ID: 442fba7a6c2a
Revises: 5e11d3f71a17
Create Date: 2025-04-11 17:41:22.366037

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '442fba7a6c2a'
down_revision: Union[str, None] = '5e11d3f71a17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
