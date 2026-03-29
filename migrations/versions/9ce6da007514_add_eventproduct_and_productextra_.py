"""Add FuelType, ProductExtra, EventProduct, and associations

Revision ID: 9ce6da007514
Revises: b3a1570d54cc
Create Date: 2026-03-29 15:04:31.595739
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9ce6da007514'
down_revision = 'b3a1570d54cc'
branch_labels = None
depends_on = None

def upgrade():
    # -------------------------
    # 1️⃣ Ensure event_product has an ID column first
    # -------------------------
    with op.batch_alter_table('event_product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), autoincrement=True))
        batch_op.create_primary_key('pk_event_product', ['id'])  # ← add this

    # -------------------------
    # 2️⃣ Update Vehicle fuel_type to be NOT NULL
    # -------------------------
    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.alter_column(
            'fuel_type',
            existing_type=postgresql.ENUM('ELECTRIC', 'PETROL', 'DIESEL', name='fueltype'),
            nullable=False
        )

    # -------------------------
    # 3️⃣ Create ProductExtra table
    # -------------------------
    op.create_table(
        'product_extra',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(120), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('product.id'), nullable=False)
    )

    # -------------------------
    # 4️⃣ Create EventProductExtra association table
    # -------------------------
    op.create_table(
        'event_product_extra',
        sa.Column('event_product_id', sa.Integer(), sa.ForeignKey('event_product.id')),
        sa.Column('product_extra_id', sa.Integer(), sa.ForeignKey('product_extra.id'))
    )

def downgrade():
    # -------------------------
    # Reverse order
    # -------------------------
    # 1️⃣ Drop association table first
    op.drop_table('event_product_extra')

    # 2️⃣ Drop ProductExtra table
    op.drop_table('product_extra')

    # 3️⃣ Revert Vehicle fuel_type nullable change
    with op.batch_alter_table('vehicle', schema=None) as batch_op:
        batch_op.alter_column(
            'fuel_type',
            existing_type=postgresql.ENUM('ELECTRIC', 'PETROL', 'DIESEL', name='fueltype'),
            nullable=True
        )

    # 4️⃣ Remove ID column from event_product
    with op.batch_alter_table('event_product', schema=None) as batch_op:
        batch_op.drop_constraint('pk_event_product', type_='primary')  # ← add this
        batch_op.drop_column('id')