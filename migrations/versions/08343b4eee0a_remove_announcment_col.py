"""remove announcment col

Revision ID: 08343b4eee0a
Revises: cf2e81a7d960
Create Date: 2019-07-16 14:51:21.996349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08343b4eee0a'
down_revision = 'cf2e81a7d960'
branch_labels = None
depends_on = None


def upgrade():
  pass
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_column('membernewspost', 'is_announcement')
    # op.create_index(op.f('ix_user_userAccess'), 'user', ['userAccess'], unique=False)
    # op.drop_index('ix_user_userAccess', table_name='user')
    # ### end Alembic commands ###


def downgrade():
  pass
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_index('ix_user_userAccess', 'user', ['userAccess'], unique=False)
    # op.drop_index(op.f('ix_user_userAccess'), table_name='user')
    # op.add_column('membernewspost', sa.Column('is_announcement', sa.BOOLEAN(), nullable=True))
    # ### end Alembic commands ###