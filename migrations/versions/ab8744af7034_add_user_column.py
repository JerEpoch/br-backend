"""add user column

Revision ID: ab8744af7034
Revises: 2aa82f725608
Create Date: 2019-04-01 15:54:09.687309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab8744af7034'
down_revision = '2aa82f725608'
branch_labels = None
depends_on = None


def upgrade():
  pass
    # ### commands auto generated by Alembic - please adjust! ###
    #op.add_column('membernewspost', sa.Column('user', sa.String(), nullable=False, server_default='thing'))
    #op.alter_column('membernewspost', 'user', server_default=None)
    # op.create_index(op.f('ix_user_userAccess'), 'user', ['userAccess'], unique=False)
    # op.drop_index('ix_user_userAccess', table_name='user')
    # ### end Alembic commands ###


def downgrade():
  pass
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_index('ix_user_userAccess', 'user', ['userAccess'], unique=False)
    # op.drop_index(op.f('ix_user_userAccess'), table_name='user')
    #op.drop_column('membernewspost', 'user')
    # ### end Alembic commands ###