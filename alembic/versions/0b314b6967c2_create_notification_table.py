"""Create notification table

Revision ID: 0b314b6967c2
Revises: e0d5fa494a23
Create Date: 2023-05-08 12:11:08.981901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b314b6967c2'
down_revision = 'e0d5fa494a23'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'notification',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('sender_id', sa.Integer(), nullable=False),
        sa.Column('recipient_id', sa.Integer(), nullable=False),
        sa.Column('message', sa.String, nullable=False),
        sa.ForeignKeyConstraint(['sender_id'], ['users.id']),
        sa.ForeignKeyConstraint(['recipient_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    pass


def downgrade() -> None:
    op.drop_table('notification')
    pass
