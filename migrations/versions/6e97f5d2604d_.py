"""empty message

Revision ID: 6e97f5d2604d
Revises: 
Create Date: 2024-03-13 10:07:02.228417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e97f5d2604d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.Column('freshbooks_id', sa.Integer(), nullable=False),
    sa.Column('created_ts', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_client_created_ts'), ['created_ts'], unique=False)
        batch_op.create_index(batch_op.f('ix_client_email'), ['email'], unique=True)

    op.create_table('community',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('client_notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('client_notes', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_client_notes_client_id'), ['client_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_client_notes_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('client_notes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_client_notes_timestamp'))
        batch_op.drop_index(batch_op.f('ix_client_notes_client_id'))

    op.drop_table('client_notes')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    op.drop_table('community')
    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_client_email'))
        batch_op.drop_index(batch_op.f('ix_client_created_ts'))

    op.drop_table('client')
    # ### end Alembic commands ###
