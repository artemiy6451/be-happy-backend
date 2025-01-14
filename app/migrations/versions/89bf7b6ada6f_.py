"""empty message

Revision ID: 89bf7b6ada6f
Revises: 223462abd4c0
Create Date: 2024-12-29 18:18:07.857365

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "89bf7b6ada6f"
down_revision: Union[str, None] = "223462abd4c0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "cards",
        "last_used_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
    )
    op.alter_column(
        "user_buildings",
        "last_used_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user_buildings",
        "last_used_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
    )
    op.alter_column(
        "cards",
        "last_used_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
