"""empty message

Revision ID: c8c7ea47745c
Revises: 117dfd6d1367
Create Date: 2024-12-29 16:51:54.556914

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c8c7ea47745c"
down_revision: Union[str, None] = "117dfd6d1367"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "buildings",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("income", sa.Integer(), nullable=False),
        sa.Column("cost", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("buildings")
    # ### end Alembic commands ###
