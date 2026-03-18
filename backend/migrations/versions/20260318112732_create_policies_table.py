"""Create policies table

Revision ID: 20260318112732
Revises:
Create Date: Y-03-18 11:27:32.%f

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260318112732'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'policies',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', sa.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('plan_name', sa.String(100), nullable=False),
        sa.Column('premium_amount', sa.Numeric(10, 2), nullable=False, server_default='0.00'),
        sa.Column('coverage_amount', sa.Numeric(12, 2), nullable=False, server_default='0.00'),
        sa.Column('status', sa.Enum('active', 'cancelled', 'expired', name='policy_status'), server_default='active', nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), onupdate=sa.func.now())
    )

    op.create_index('ix_policies_user_id', 'policies', ['user_id'])
    op.create_index('ix_policies_user_plan', 'policies', ['user_id', 'plan_name'], unique=True)

def downgrade():
    op.drop_index('ix_policies_user_plan')
    op.drop_index('ix_policies_user_id')
    op.drop_table('policies')
    op.execute('DROP TYPE IF EXISTS policy_status')
