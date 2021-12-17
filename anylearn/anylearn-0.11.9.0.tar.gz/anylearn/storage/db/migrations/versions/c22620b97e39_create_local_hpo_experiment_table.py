"""create local hpo experiment table

Revision ID: c22620b97e39
Revises: 6dfd859f129e
Create Date: 2021-05-18 17:32:53.814373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c22620b97e39'
down_revision = '6dfd859f129e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('local_hpo_experiment',
    sa.Column('id', sa.String(length=8), nullable=False),
    sa.Column('port', sa.Integer(), nullable=False),
    sa.Column('mode', sa.String(length=8), nullable=False),
    sa.Column('status', sa.String(length=16), nullable=False),
    sa.Column('project_id', sa.String(length=32), nullable=False),
    sa.Column('project_name', sa.String(length=255), nullable=False),
    sa.Column('algorithm_id', sa.String(length=32), nullable=False),
    sa.Column('algorithm_dir', sa.String(length=4096), nullable=True),
    sa.Column('algorithm_archive', sa.String(length=4096), nullable=True),
    sa.Column('dataset_id', sa.String(length=32), nullable=False),
    sa.Column('dataset_dir', sa.String(length=4096), nullable=True),
    sa.Column('dataset_archive', sa.String(length=4096), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('local_hpo_experiment')
    # ### end Alembic commands ###
