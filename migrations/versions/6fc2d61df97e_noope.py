"""noope

Revision ID: 6fc2d61df97e
Revises: b161fa81e182
Create Date: 2022-02-02 02:43:36.821532

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '6fc2d61df97e'
down_revision = 'b161fa81e182'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('patient', sqlmodel.Column('age', sqlmodel.Integer(), nullable=True))
    op.create_index(op.f('ix_patient_age'), 'patient', ['age'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_patient_age'), table_name='patient')
    op.drop_column('patient', 'age')
