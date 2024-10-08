"""add table_args às tabelas event_colab e sub_event_colab

Revision ID: 694dfd6225da
Revises: 24f6dd9b3b71
Create Date: 2024-10-09 10:09:48.593121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '694dfd6225da'
down_revision = '24f6dd9b3b71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sub_event_colabs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_colab_id', sa.Integer(), nullable=False),
    sa.Column('sub_event_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_colab_id'], ['event_colabs.id'], ),
    sa.ForeignKeyConstraint(['sub_event_id'], ['sub_events.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('event_colab_id', 'sub_event_id', name='colab_already_in_this_sub_event')
    )
    with op.batch_alter_table('event_colabs', schema=None) as batch_op:
        batch_op.create_unique_constraint('colab_already_in_this_event', ['colab_id', 'event_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event_colabs', schema=None) as batch_op:
        batch_op.drop_constraint('colab_already_in_this_event', type_='unique')

    op.drop_table('sub_event_colabs')
    # ### end Alembic commands ###
