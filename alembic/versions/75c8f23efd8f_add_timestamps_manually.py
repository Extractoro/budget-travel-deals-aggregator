"""Add timestamps manually

Revision ID: 75c8f23efd8f
Revises: 8c204f4b8f2f
Create Date: 2025-06-09 22:13:58.958722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75c8f23efd8f'
down_revision: Union[str, None] = '8c204f4b8f2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(timezone=True)))
    op.add_column('data_results', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')))
    op.add_column('data_results', sa.Column('updated_at', sa.DateTime(timezone=True)))
    op.add_column('subscriptions', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')))
    op.add_column('subscriptions', sa.Column('updated_at', sa.DateTime(timezone=True)))

def downgrade():
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'updated_at')
    op.drop_column('data_results', 'created_at')
    op.drop_column('data_results', 'updated_at')
    op.drop_column('subscriptions', 'created_at')
    op.drop_column('subscriptions', 'updated_at')
