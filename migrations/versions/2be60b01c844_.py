"""empty message

Revision ID: 2be60b01c844
Revises: 1488d90762b2
Create Date: 2019-05-08 08:23:55.823878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2be60b01c844'
down_revision = '1488d90762b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Account', sa.Column('admin', sa.Boolean(), server_default='False', nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Account', 'admin')
    # ### end Alembic commands ###