"""User tokens

Revision ID: 534cf282ddb0
Revises: 9c7ec9ef7a73
Create Date: 2023-08-28 18:50:05.863713

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '534cf282ddb0'
down_revision = '9c7ec9ef7a73'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('token_expiration', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_user_token'), ['token'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_token'))
        batch_op.drop_column('token_expiration')
        batch_op.drop_column('token')

    # ### end Alembic commands ###