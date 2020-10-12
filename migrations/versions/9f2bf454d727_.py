"""empty message

Revision ID: 9f2bf454d727
Revises: 9bd99dde22e0
Create Date: 2020-10-10 21:35:09.539382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f2bf454d727'
down_revision = '9bd99dde22e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Association',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['actor_id'], ['actor.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Association')
    # ### end Alembic commands ###
