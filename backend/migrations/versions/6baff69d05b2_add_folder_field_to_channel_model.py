"""add folder field to channel model

Revision ID: 6baff69d05b2
Revises: 20e43bf62411
Create Date: 2023-10-22 15:41:34.655519

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6baff69d05b2"
down_revision = "20e43bf62411"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "channels",
        sa.Column(
            "local_folder", sa.String(length=250), nullable=False, server_default=""
        ),
    )


def downgrade() -> None:
    op.drop_column("channels", "local_folder")
