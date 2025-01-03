"""empty message

Revision ID: 1d83c89ce167
Revises: 58679fc0759f
Create Date: 2025-01-03 14:38:11.306772

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1d83c89ce167"
down_revision: Union[str, None] = "58679fc0759f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("level", sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "level")
    # ### end Alembic commands ###
