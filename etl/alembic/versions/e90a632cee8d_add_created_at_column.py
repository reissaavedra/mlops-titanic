"""add created_at column

Revision ID: e90a632cee8d
Revises: b4dbf82bc918
Create Date: 2023-05-06 23:07:50.690385

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import DateTime

# revision identifiers, used by Alembic.
revision = 'e90a632cee8d'
down_revision = 'b4dbf82bc918'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('titanic',
                  sa.Column('created_at', sa.DateTime(timezone=True),
                            nullable=True, server_default=sa.text('(now() at time zone \'utc-5\')')))


def downgrade() -> None:
    op.drop_column('titanic',
                   'created_at')
