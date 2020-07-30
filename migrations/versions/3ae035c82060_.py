"""empty message

Revision ID: 3ae035c82060
Revises: e340f1d6ae4f
Create Date: 2020-07-25 21:44:46.296239

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3ae035c82060'
down_revision = 'e340f1d6ae4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('alarm', 'breathing',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=True)
    op.alter_column('alarm', 'decibel_level',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('alarm', 'decibel_level',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.alter_column('alarm', 'breathing',
               existing_type=mysql.TINYINT(display_width=1),
               nullable=False)
    # ### end Alembic commands ###