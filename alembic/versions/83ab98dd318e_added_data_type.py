"""Added data_type

Revision ID: 83ab98dd318e
Revises: df8fa3a4a234
Create Date: 2025-06-08 15:31:47.730267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83ab98dd318e'
down_revision: Union[str, None] = 'df8fa3a4a234'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

data_type_enum = sa.Enum('HOTEL', 'FLIGHT', 'ONEWAY_FLIGHT', name='datatypeenum')


def upgrade() -> None:
    """Upgrade schema."""
    data_type_enum.create(op.get_bind())
    op.add_column('data_results', sa.Column('data_type', data_type_enum, nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('data_results', 'data_type')
    data_type_enum.drop(op.get_bind())