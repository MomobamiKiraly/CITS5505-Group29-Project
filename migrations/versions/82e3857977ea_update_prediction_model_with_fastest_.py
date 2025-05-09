"""Update Prediction model with fastest_lap, restore old fields

Revision ID: 82e3857977ea
Revises: 4051f940e9a4
Create Date: 2025-05-08 00:03:43.553904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82e3857977ea'
down_revision = '4051f940e9a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prediction', schema=None) as batch_op:
        batch_op.add_column(sa.Column('race_name', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('actual_winner', sa.String(length=80), nullable=True))
        batch_op.add_column(sa.Column('points', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('prediction', schema=None) as batch_op:
        batch_op.drop_column('points')
        batch_op.drop_column('actual_winner')
        batch_op.drop_column('race_name')

    # ### end Alembic commands ###
