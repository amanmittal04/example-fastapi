"""empty message

Revision ID: 5235dc1be8d5
Revises: 0b314b6967c2
Create Date: 2023-05-08 12:25:12.719091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5235dc1be8d5'
down_revision = '0b314b6967c2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notification')
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_table('notification',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('sender_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('recipient_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('message', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], name='notification_recipient_id_fkey'),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], name='notification_sender_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='notification_pkey')
    )
    # ### end Alembic commands ###
