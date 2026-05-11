"""add_destacado_to_post

Revision ID: f18607fe3630
Revises: 674c57391df0
Create Date: 2026-05-02 23:54:03.450190

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f18607fe3630'
down_revision: Union[str, Sequence[str], None] = '674c57391df0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Solo agrega la columna destacado; las otras ya existen en la BD.
    op.add_column('post', sa.Column('destacado', sa.Boolean(), server_default='0', nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('post', 'destacado')
