"""add foreign key to posts table

Revision ID: 67b4b3f4bcb3
Revises: 4aa803dd7f19
Create Date: 2023-05-04 10:41:23.915148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67b4b3f4bcb3'
down_revision = '4aa803dd7f19'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
