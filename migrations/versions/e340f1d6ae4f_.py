"""empty message

Revision ID: e340f1d6ae4f
Revises: 7efa4e875494
Create Date: 2020-07-25 21:06:09.105312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e340f1d6ae4f'
down_revision = '7efa4e875494'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alarm', sa.Column('decibel_level', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('alarm', 'decibel_level')
    # ### end Alembic commands ###