"""Mein Kommentar zur anpassung 

Revision ID: c0bda6f73910
Revises: 2ac6b2503e95
Create Date: 2023-09-01 12:40:22.558077

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c0bda6f73910'
down_revision = '2ac6b2503e95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('inputTitle', sa.String(length=1000), nullable=True),
    sa.Column('inputPost', sa.String(length=10000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('inputTitle')
        batch_op.drop_column('inputPost')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('inputPost', mysql.VARCHAR(length=10000), nullable=True))
        batch_op.add_column(sa.Column('inputTitle', mysql.VARCHAR(length=1000), nullable=True))

    op.drop_table('post_model')
    # ### end Alembic commands ###
