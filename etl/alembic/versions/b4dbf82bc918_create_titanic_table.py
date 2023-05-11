"""create titanic table

Revision ID: b4dbf82bc918
Revises: 
Create Date: 2023-05-06 11:57:11.290369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4dbf82bc918'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        'titanic',
        sa.Column('passenger_id', sa.Integer, primary_key=True),
        sa.Column('survived', sa.Integer, nullable=True),
        sa.Column('p_class', sa.SmallInteger, nullable=False),
        sa.Column('name', sa.String(250), nullable=False),
        sa.Column('sex', sa.String(20), nullable=False),
        sa.Column('age', sa.Float, nullable=True),
        sa.Column('sib_sp', sa.SmallInteger, nullable=True),
        sa.Column('parch', sa.SmallInteger, nullable=True),
        sa.Column('ticket', sa.String(50), nullable=True),
        sa.Column('fare', sa.Float, nullable=True),
        sa.Column('cabin', sa.String(20), nullable=True),
        sa.Column('embarked', sa.String(20), nullable=True)
    )


def downgrade() -> None:
    op.drop_table('titanic')
