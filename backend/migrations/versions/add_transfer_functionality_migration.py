"""Add transaction table and limits to accounts

Revision ID: 001_add_transfer_functionality
Revises: initial
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from decimal import Decimal

# revision identifiers, used by Alembic.
revision = '001_add_transfer_functionality'
down_revision = 'initial'
branch_labels = None
depends_on = None

def upgrade():
    # Add transfer limit columns to accounts table
    op.add_column('accounts', sa.Column('daily_transfer_limit', sa.Numeric(15, 2), nullable=False, server_default=str(Decimal('50000'))))
    op.add_column('accounts', sa.Column('monthly_transfer_limit', sa.Numeric(15, 2), nullable=False, server_default=str(Decimal('500000'))))

    # Create transactions table
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('from_account_id', sa.Integer(), nullable=False),
        sa.Column('to_account_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Numeric(15, 2), nullable=False),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('transaction_type', sa.String(), nullable=False, server_default='transfer'),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['from_account_id'], ['accounts.id']),
        sa.ForeignKeyConstraint(['to_account_id'], ['accounts.id']),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for performance
    op.create_index('ix_transactions_from_account', 'transactions', ['from_account_id'])
    op.create_index('ix_transactions_to_account', 'transactions', ['to_account_id'])
    op.create_index('ix_transactions_created_at', 'transactions', ['created_at'])

def downgrade():
    # Drop transaction table and indexes
    op.drop_index('ix_transactions_created_at', table_name='transactions')
    op.drop_index('ix_transactions_to_account', table_name='transactions')
    op.drop_index('ix_transactions_from_account', table_name='transactions')
    op.drop_table('transactions')

    # Drop transfer limit columns
    op.drop_column('accounts', 'monthly_transfer_limit')
    op.drop_column('accounts', 'daily_transfer_limit')
