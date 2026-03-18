"""Create ledger table

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create ledger table with all required fields
    op.create_table(
        'ledger',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('event_type', sa.VARCHAR(50), nullable=False),
        sa.Column('transfer_id', sa.BigInteger(), nullable=False),
        sa.Column('from_account_id', sa.BigInteger(), nullable=False),
        sa.Column('to_account_id', sa.BigInteger(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('from_balance_before', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('from_balance_after', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('to_balance_before', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('to_balance_after', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('audit_data', postgresql.JSONB(astext_type=sa.Text()), server_default='{}', nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('idx_ledger_transfer_id', 'ledger', ['transfer_id'])
    op.create_index('idx_ledger_from_account', 'ledger', ['from_account_id'])
    op.create_index('idx_ledger_to_account', 'ledger', ['to_account_id'])
    op.create_index('idx_ledger_created_at', 'ledger', [sa.text('created_at DESC')])

def downgrade():
    # Drop indexes
    op.drop_index('idx_ledger_created_at', table_name='ledger')
    op.drop_index('idx_ledger_to_account', table_name='ledger')
    op.drop_index('idx_ledger_from_account', table_name='ledger')
    op.drop_index('idx_ledger_transfer_id', table_name='ledger')

    # Drop table
    op.drop_table('ledger')
