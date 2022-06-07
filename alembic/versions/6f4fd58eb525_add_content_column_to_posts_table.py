"""add content column to posts table

Revision ID: 6f4fd58eb525
Revises: 638e7ba192ad
Create Date: 2022-06-06 18:30:57.623259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f4fd58eb525'
down_revision = '638e7ba192ad'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts' , sa.Column('content', sa.String, nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
