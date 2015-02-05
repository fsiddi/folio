"""table for social links

Revision ID: 3f9d11960212
Revises: 499b785652a1
Create Date: 2015-02-05 21:56:44.491438

"""

# revision identifiers, used by Alembic.
revision = '3f9d11960212'
down_revision = '499b785652a1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('social_link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('icon', sa.String(length=16), nullable=False),
    sa.Column('handle', sa.String(length=128), nullable=False),
    sa.Column('href', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('social_link')

