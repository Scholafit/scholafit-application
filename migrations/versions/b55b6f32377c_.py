"""empty message

Revision ID: b55b6f32377c
Revises: 
Create Date: 2024-09-23 21:02:32.390795

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b55b6f32377c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profiles',
    sa.Column('subscription_status', mysql.ENUM('ACTIVE', 'INACTIVE'), nullable=False),
    sa.Column('isAdult', sa.Boolean(), nullable=False),
    sa.Column('current_education_level', sa.String(length=120), nullable=False),
    sa.Column('school_name', sa.String(length=120), nullable=True),
    sa.Column('expected_graduation_year', sa.String(length=4), nullable=True),
    sa.Column('desired_course', sa.String(length=120), nullable=True),
    sa.Column('university_choices', sa.JSON(), nullable=True),
    sa.Column('country', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('postal_code', sa.String(length=60), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('parent_first_name', sa.String(length=120), nullable=True),
    sa.Column('parent_last_name', sa.String(length=120), nullable=True),
    sa.Column('parent_email', sa.String(length=120), nullable=True),
    sa.Column('parent_phone_number', sa.String(length=15), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student',
    sa.Column('firstname', sa.String(length=100), nullable=False),
    sa.Column('lastname', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('users',
    sa.Column('username', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('profile_data', sa.JSON(), nullable=True),
    sa.Column('roles', sa.JSON(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('student')
    op.drop_table('profiles')
    # ### end Alembic commands ###