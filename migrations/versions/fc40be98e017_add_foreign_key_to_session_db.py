"""add foreign key to session db

Revision ID: fc40be98e017
Revises: aa675715e812
Create Date: 2022-08-01 12:28:32.348951

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, INTEGER, ForeignKey


# revision identifiers, used by Alembic.
revision = 'fc40be98e017'
down_revision = 'aa675715e812'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('session',
                  Column('user_id', INTEGER, ForeignKey('user_data.user_id'))
                  )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'session', type_='foreignkey')
    op.drop_column('session', 'user_id')
    # ### end Alembic commands ###
