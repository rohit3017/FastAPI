"""add foreign_key to posts table

Revision ID: 2c0c7fa6f71b
Revises: 50d66622129d
Create Date: 2022-06-06 18:58:24.922353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c0c7fa6f71b'
down_revision = '50d66622129d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id',sa.Integer,nullable = False))
    op.create_foreign_key('post_user_fk',source_table= 'posts', referent_table='users', local_cols=['owner_id'], remote_cols =['id'], ondelete= "CASCADE" )
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk' , table_name='posts')
    op.drop_column('posts','owner_id')
    pass
