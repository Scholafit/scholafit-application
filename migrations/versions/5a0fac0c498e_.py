"""empty message

Revision ID: 5a0fac0c498e
Revises: 7db474cb9056
Create Date: 2024-09-28 20:27:18.842745

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5a0fac0c498e'
down_revision = '7db474cb9056'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('db__passage',
    sa.Column('passage', sa.Text(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('passage_id', sa.Integer(), nullable=True))
        batch_op.drop_column('passage')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('passage', mysql.TEXT(), nullable=True))
        batch_op.drop_column('passage_id')

    op.drop_table('db__passage')
    # ### end Alembic commands ###
