"""Add sender_id to InvitationCode.

Revision ID: 11fc5ea9e16a
Revises: 9b2b4d0abcc
Create Date: 2015-04-19 12:06:41.634714

"""

# revision identifiers, used by Alembic.
revision = '11fc5ea9e16a'
down_revision = '9b2b4d0abcc'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invitation_code', sa.Column('sender_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'invitation_code', 'user', ['sender_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'invitation_code', type_='foreignkey')
    op.drop_column('invitation_code', 'sender_id')
    ### end Alembic commands ###