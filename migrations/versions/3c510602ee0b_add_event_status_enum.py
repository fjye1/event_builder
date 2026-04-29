"""add event status enum

Revision ID: 3c510602ee0b
Revises: bfedd2dcf51c
Create Date: 2026-04-29 15:38:49.551729
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '3c510602ee0b'
down_revision = 'bfedd2dcf51c'
branch_labels = None
depends_on = None


# define enum ONCE (must match model exactly)
event_status = sa.Enum(
    'generated',
    'pending',
    'confirmed',
    'cancelled',
    name='eventstatus'
)


def upgrade():
    # 1. create the enum type in Postgres
    event_status.create(op.get_bind(), checkfirst=True)

    # 2. add column using it
    with op.batch_alter_table('event') as batch_op:
        batch_op.add_column(
            sa.Column(
                'status',
                event_status,
                nullable=False,
                server_default='generated'
            )
        )


def downgrade():
    with op.batch_alter_table('event') as batch_op:
        batch_op.drop_column('status')

    # 3. remove enum type
    event_status.drop(op.get_bind(), checkfirst=True)