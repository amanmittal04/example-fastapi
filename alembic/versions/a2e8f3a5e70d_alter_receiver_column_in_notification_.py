"""alter receiver column in notification table

Revision ID: a2e8f3a5e70d
Revises: 5235dc1be8d5
Create Date: 2023-05-08 12:58:55.776646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2e8f3a5e70d'
down_revision = '5235dc1be8d5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('notification', 'recipient_id',
                    new_column_name=sa.Column('receiver_id', sa.Integer))
    pass


def downgrade() -> None:
    op.alter_column('notification', 'receiver_id',
                    new_column_name=sa.Column('recipient_id', sa.Integer))
    pass
