"""initial

Revision ID: 6f6aa1df4b63
Revises: 
Create Date: 2023-05-19 15:30:37.441942

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '6f6aa1df4b63'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profiles',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('patronymic', sa.String(length=255), nullable=True),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='content'
    )
    op.create_table('profile_movies',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('movie_id', sa.UUID(), nullable=True),
    sa.Column('profile_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['content.profiles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='content'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profile_movies', schema='content')
    op.drop_table('profiles', schema='content')
    # ### end Alembic commands ###
