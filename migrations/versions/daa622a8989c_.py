"""empty message

Revision ID: daa622a8989c
Revises: 4d6cdda88ff7
Create Date: 2020-07-23 18:22:42.117644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'daa622a8989c'
down_revision = '4d6cdda88ff7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alarm', sa.Column('created_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('alarm', 'created_date')
    # ### end Alembic commands ###