"""Restore 4051 initial migration

Revision ID: 4051f940e9a4
Revises: 831d00dec985
Create Date: 2025-05-16
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = '4051f940e9a4'
down_revision = '831d00dec985'
branch_labels = None
depends_on = None

def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_tables = inspector.get_table_names()

    if 'user' not in existing_tables:
        op.create_table(
            'user',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('username', sa.String(length=64), nullable=False),
            sa.Column('email', sa.String(length=120), nullable=False),
            sa.Column('password_hash', sa.String(length=128), nullable=False),
            sa.Column('favorite_team', sa.String(length=64), nullable=True),
            sa.Column('favorite_driver', sa.String(length=64), nullable=True),
            sa.Column('bio', sa.Text(), nullable=True, server_default=''),
            sa.Column('profile_pic', sa.String(length=256), nullable=True, server_default='default.jpg'),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('username'),
            sa.UniqueConstraint('email')
        )

    if 'prediction' not in existing_tables:
        op.create_table(
            'prediction',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('race_name', sa.String(length=120), nullable=True),
            sa.Column('predicted_winner', sa.String(length=80), nullable=True),
            sa.Column('fastest_lap', sa.String(length=80), nullable=True),
            sa.Column('actual_winner', sa.String(length=80), nullable=True),
            sa.Column('points', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['user_id'], ['user.id']),
            sa.PrimaryKeyConstraint('id')
        )

    if 'friendship' not in existing_tables:
        op.create_table(
            'friendship',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('follower_id', sa.Integer(), nullable=False),
            sa.Column('followed_id', sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(['follower_id'], ['user.id']),
            sa.ForeignKeyConstraint(['followed_id'], ['user.id']),
            sa.UniqueConstraint('follower_id', 'followed_id', name='unique_friendship'),
            sa.PrimaryKeyConstraint('id')
        )

    if 'blog_post' not in existing_tables:
        op.create_table(
            'blog_post',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('author_id', sa.Integer(), nullable=False),
            sa.Column('title', sa.String(length=100), nullable=False),
            sa.Column('content', sa.Text(), nullable=False),
            sa.Column('timestamp', sa.DateTime(), nullable=True),
            sa.Column('is_public', sa.Boolean(), nullable=True, server_default=sa.text('1')),
            sa.ForeignKeyConstraint(['author_id'], ['user.id']),
            sa.PrimaryKeyConstraint('id')
        )

    if 'chat_message' not in existing_tables:
        op.create_table(
            'chat_message',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('sender_id', sa.Integer(), nullable=False),
            sa.Column('receiver_id', sa.Integer(), nullable=False),
            sa.Column('content', sa.Text(), nullable=False),
            sa.Column('timestamp', sa.DateTime(), nullable=True),
            sa.Column('is_read', sa.Boolean(), nullable=True, server_default=sa.text('0')),
            sa.ForeignKeyConstraint(['sender_id'], ['user.id']),
            sa.ForeignKeyConstraint(['receiver_id'], ['user.id']),
            sa.PrimaryKeyConstraint('id')
        )

def downgrade():
    op.drop_table('chat_message')
    op.drop_table('blog_post')
    op.drop_table('friendship')
    op.drop_table('prediction')
    op.drop_table('user')