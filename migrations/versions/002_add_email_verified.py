from alembic import op
import sqlalchemy as sa


revision = '002_add_email_verified'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email_verified', sa.Boolean(), nullable=True, server_default='0'))
    
    op.execute("UPDATE users SET email_verified = 0 WHERE email_verified IS NULL")


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('email_verified')
