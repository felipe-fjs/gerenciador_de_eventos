"""adicionando coluna completed à tabela de user_profiles, para sinalizar que o usuário já completou o perfil

Revision ID: 95f5d96d3c4f
Revises: d732e7c159a6
Create Date: 2024-11-14 20:13:32.979440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95f5d96d3c4f'
down_revision = 'd732e7c159a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('completed', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.drop_column('completed')

    # ### end Alembic commands ###
