"""empty message

Revision ID: 280a955157eb
Revises: 56cbe4f3969d
Create Date: 2020-07-21 02:33:33.914050

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '280a955157eb'
down_revision = '56cbe4f3969d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('jwt', table_name='user')
    op.drop_column('user', 'jwt')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('jwt', mysql.VARCHAR(length=160), nullable=True))
    op.create_index('jwt', 'user', ['jwt'], unique=True)
    # ### end Alembic commands ###
