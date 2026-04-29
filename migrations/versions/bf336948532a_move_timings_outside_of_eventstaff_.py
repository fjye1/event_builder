"""move timings outside of eventstaff logic and into event model

Revision ID: bf336948532a
Revises: 3c510602ee0b
Create Date: 2026-04-29 16:16:27.157618

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'bf336948532a'
down_revision = '3c510602ee0b'
branch_labels = None
depends_on = None

# define enum explicitly
arrival_mode = sa.Enum(
    "unit",
    "venue",
    name="arrivalmode"
)

def upgrade():
    # ### EVENT TABLE ###
    with op.batch_alter_table('event') as batch_op:
        batch_op.add_column(sa.Column('arrive_unit_time', sa.Time(), nullable=True))
        batch_op.add_column(sa.Column('leave_unit_time', sa.Time(), nullable=True))
        batch_op.add_column(sa.Column('arrive_venue_time', sa.Time(), nullable=True))
        batch_op.add_column(sa.Column('service_start_time', sa.Time(), nullable=True))
        batch_op.add_column(sa.Column('service_end_time', sa.Time(), nullable=True))

    # ### CREATE ENUM FIRST (IMPORTANT FIX) ###
    arrival_mode.create(op.get_bind(), checkfirst=True)

    # ### EVENT_STAFF TABLE ###
    with op.batch_alter_table('event_staff') as batch_op:
        batch_op.add_column(
            sa.Column(
                'arrival_mode',
                arrival_mode,
                nullable=False,
                server_default="unit"
            )
        )
        batch_op.drop_column('arrive_venue_time')
        batch_op.drop_column('arrive_unit_time')


def downgrade():
    with op.batch_alter_table('event_staff') as batch_op:
        batch_op.add_column(sa.Column('arrive_unit_time', sa.Time(), nullable=True))
        batch_op.add_column(sa.Column('arrive_venue_time', sa.Time(), nullable=True))
        batch_op.drop_column('arrival_mode')

    # drop enum safely
    arrival_mode.drop(op.get_bind(), checkfirst=True)

    with op.batch_alter_table('event') as batch_op:
        batch_op.drop_column('service_end_time')
        batch_op.drop_column('service_start_time')
        batch_op.drop_column('arrive_venue_time')
        batch_op.drop_column('leave_unit_time')
        batch_op.drop_column('arrive_unit_time')
