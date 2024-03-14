"""empty message

Revision ID: ec92db30b96a
Revises: a2a3a5d263c7
Create Date: 2024-03-13 12:02:41.265861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec92db30b96a'
down_revision = 'a2a3a5d263c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ads', schema=None) as batch_op:
        batch_op.add_column(sa.Column('community', sa.String(length=24), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('ads', schema=None) as batch_op:
        batch_op.drop_column('community')

    # ### end Alembic commands ###
