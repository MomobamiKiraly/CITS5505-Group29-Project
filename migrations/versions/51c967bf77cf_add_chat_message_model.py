"""Add chat message model

Revision ID: 51c967bf77cf
Revises: 82e3857977ea
Create Date: 2025-05-15 13:00:00.173350
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '51c967bf77cf'
down_revision = '82e3857977ea'
branch_labels = None
depends_on = None

def upgrade():
    # Table already created in a prior migration (4051f940e9a4), so no action needed
    pass

def downgrade():
    # Don't drop the table here to preserve consistency with the earlier migration
    pass
