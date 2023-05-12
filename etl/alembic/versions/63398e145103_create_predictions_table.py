"""create predictions table

Revision ID: 63398e145103
Revises: e90a632cee8d
Create Date: 2023-05-08 07:15:05.831743

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '63398e145103'
down_revision = 'e90a632cee8d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'survived_predictions',
        sa.Column('passenger_id', sa.Integer, nullable=False),
        sa.Column('predict', sa.SmallInteger, nullable=False),
        sa.Column('model', sa.String, nullable=False),
        sa.PrimaryKeyConstraint('passenger_id', 'model', name='pk_my_table')
    )


def downgrade() -> None:
    op.drop_table('survived_predictions')
