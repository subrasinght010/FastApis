"""Initial migration

Revision ID: 6e26ca205531
Revises: 
Create Date: 2025-02-01 16:08:53.373534

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e26ca205531'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('access_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_access_log_id'), 'access_log', ['id'], unique=False)
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_id'), 'category', ['id'], unique=False)
    op.create_index(op.f('ix_category_name'), 'category', ['name'], unique=True)
    op.create_table('review_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('stars', sa.Integer(), nullable=True),
    sa.Column('review_id', sa.String(length=255), nullable=True),
    sa.Column('tone', sa.String(length=255), nullable=True),
    sa.Column('sentiment', sa.String(length=255), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_review_history_id'), 'review_history', ['id'], unique=False)
    op.create_index(op.f('ix_review_history_review_id'), 'review_history', ['review_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_review_history_review_id'), table_name='review_history')
    op.drop_index(op.f('ix_review_history_id'), table_name='review_history')
    op.drop_table('review_history')
    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.drop_index(op.f('ix_category_id'), table_name='category')
    op.drop_table('category')
    op.drop_index(op.f('ix_access_log_id'), table_name='access_log')
    op.drop_table('access_log')
    # ### end Alembic commands ###
