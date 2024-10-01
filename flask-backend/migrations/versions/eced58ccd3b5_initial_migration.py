"""Initial migration

Revision ID: eced58ccd3b5
Revises: 
Create Date: 2024-09-30 20:15:04.454868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eced58ccd3b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('app_user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('produce',
    sa.Column('produce_id', sa.Integer(), nullable=False),
    sa.Column('produce_name', sa.String(length=50), nullable=False),
    sa.Column('unit', sa.String(length=20), nullable=True),
    sa.Column('common_expdate', sa.Integer(), nullable=True),
    sa.Column('co2', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('produce_id')
    )
    op.create_table('userandproduce',
    sa.Column('userproduce_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('produce_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('purchase_date', sa.Date(), nullable=False),
    sa.Column('expiration_date', sa.Date(), nullable=False),
    sa.Column('image_url', sa.String(length=250), nullable=True),
    sa.ForeignKeyConstraint(['produce_id'], ['produce.produce_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['app_user.user_id'], ),
    sa.PrimaryKeyConstraint('userproduce_id')
    )
    op.create_table('userwastesaving',
    sa.Column('user_waste_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('amount_saved', sa.Float(), nullable=False),
    sa.Column('co2_saved', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['app_user.user_id'], ),
    sa.PrimaryKeyConstraint('user_waste_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('userwastesaving')
    op.drop_table('userandproduce')
    op.drop_table('produce')
    op.drop_table('app_user')
    # ### end Alembic commands ###
