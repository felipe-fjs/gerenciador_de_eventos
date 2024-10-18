"""adicionando tabela user_type; removendo unci_student e adicionando user_type à tabela user_profiles

Revision ID: a6bb30323a2c
Revises: fd1f940dbfb8
Create Date: 2024-10-16 18:36:12.582180

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a6bb30323a2c'
down_revision = 'fd1f940dbfb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_type', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'user_types', ['user_type'], ['id'])
        batch_op.drop_column('unci_student')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unci_student', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_type')

    op.drop_table('user_types')
    # ### end Alembic commands ###