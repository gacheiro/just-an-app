"""empty message

Revision ID: 2d0a5c70386c
Revises: 74d4a9d4c839
Create Date: 2019-11-22 19:34:39.263009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d0a5c70386c'
down_revision = '74d4a9d4c839'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usuario', sa.Column('foto_url', sa.String(length=80), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usuario', 'foto_url')
    # ### end Alembic commands ###