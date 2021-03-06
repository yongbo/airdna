"""Add qrcode to Piece.

Revision ID: 458dc7cf9150
Revises: 12e707edf972
Create Date: 2015-03-28 18:36:40.703677

"""

# revision identifiers, used by Alembic.
revision = '458dc7cf9150'
down_revision = '12e707edf972'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('piece', sa.Column('qrcode', sa.String(length=200), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('piece', 'qrcode')
    ### end Alembic commands ###
