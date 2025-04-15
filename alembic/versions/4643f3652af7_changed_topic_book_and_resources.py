"""Changed topic, book and resources

Revision ID: 4643f3652af7
Revises: e00647385def
Create Date: 2025-04-12 14:59:27.315665

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4643f3652af7'
down_revision: Union[str, None] = 'e00647385def'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
