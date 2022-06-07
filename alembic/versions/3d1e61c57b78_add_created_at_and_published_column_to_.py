"""add created at and published column to posts table

Revision ID: 3d1e61c57b78
Revises: 2c0c7fa6f71b
Create Date: 2022-06-07 15:35:06.966123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d1e61c57b78'
down_revision = '2c0c7fa6f71b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default = sa.text('now()'),nullable=True),)
    op.add_column('posts',
                    sa.Column('published', sa.Boolean(),server_default = 'TRUE', nullable= False))
    pass


def downgrade() -> None:
    op.drop_column('posts','created_at')
    op.drop_column('posts','published')
    pass
