"""pages

Revision ID: 28e080284d0c
Revises: 5ad2a77cb0d2
Create Date: 2015-02-10 18:24:28.481099

"""

# revision identifiers, used by Alembic.
revision = '28e080284d0c'
down_revision = '5ad2a77cb0d2'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('page',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('picture', sa.String(length=80), nullable=True),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(None, 'picture', 'project', ['project_id'], ['id'])
    op.create_foreign_key(None, 'project', 'category', ['category_id'], ['id'])
    op.alter_column(u'social_link', 'order',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(u'social_link', 'order',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.drop_constraint(None, 'project', type_='foreignkey')
    op.drop_constraint(None, 'picture', type_='foreignkey')
    op.drop_table('page')
    ### end Alembic commands ###
