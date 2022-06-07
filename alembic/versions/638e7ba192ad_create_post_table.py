"""create post table

Revision ID: 638e7ba192ad
Revises: 
Create Date: 2022-06-06 18:16:45.649832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '638e7ba192ad'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts' , sa.Column('id',sa.Integer, primary_key = True, nullable = False),
                            sa.Column('title',sa.String, nullable = False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
