"""adding fields to project

Revision ID: 5ad2a77cb0d2
Revises: 3f9d11960212
Create Date: 2015-02-08 23:42:07.076965

"""

# revision identifiers, used by Alembic.
revision = '5ad2a77cb0d2'
down_revision = '3f9d11960212'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('project', sa.Column('company', sa.String(length=120), nullable=True))
    op.add_column('project', sa.Column('time_frame', sa.String(length=120), nullable=True))

def downgrade():
    # sqlite is quite crappy on removing or altering the schema
    pass
