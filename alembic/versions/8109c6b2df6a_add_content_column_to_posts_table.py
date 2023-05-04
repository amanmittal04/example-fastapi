"""add content column to  posts table

Revision ID: 8109c6b2df6a
Revises: d2c835d62327
Create Date: 2023-05-03 23:40:40.745184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8109c6b2df6a'
down_revision = 'd2c835d62327'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
