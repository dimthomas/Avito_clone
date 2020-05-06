"""empty message

Revision ID: 4a15bf1a1a15
Revises: 00a6a8b9d2ab
Create Date: 2020-04-26 10:37:17.973188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a15bf1a1a15'
down_revision = '00a6a8b9d2ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('motorcycles', sa.Column('published', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('motorcycles', 'published')
    # ### end Alembic commands ###
