"""first

Revision ID: 2c3e4b8615ed
Revises: 
Create Date: 2016-12-11 16:07:28.797296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c3e4b8615ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('sex', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # add by me
    with op.batch_alter_table('posts') as batch_op:
        batch_op.drop_column('tags')
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_column('users', 'sex')
    # ### end Alembic commands ###
