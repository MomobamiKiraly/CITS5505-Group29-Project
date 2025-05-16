"""Update Prediction model with fastest_lap, restore old fields

Revision ID: 82e3857977ea
Revises: 4051f940e9a4
Create Date: 2025-05-16
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = '82e3857977ea'
down_revision = '4051f940e9a4'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    columns = [col["name"] for col in inspector.get_columns("prediction")]

    with op.batch_alter_table('prediction') as batch_op:
        if "race_name" not in columns:
            batch_op.add_column(sa.Column('race_name', sa.String(length=120)))
        if "fastest_lap" not in columns:
            batch_op.add_column(sa.Column('fastest_lap', sa.String(length=80)))
        if "actual_winner" not in columns:
            batch_op.add_column(sa.Column('actual_winner', sa.String(length=80)))
        if "points" not in columns:
            batch_op.add_column(sa.Column('points', sa.Integer))


def downgrade():
    with op.batch_alter_table('prediction') as batch_op:
        batch_op.drop_column('points')
        batch_op.drop_column('actual_winner')
        batch_op.drop_column('fastest_lap')
        batch_op.drop_column('race_name')