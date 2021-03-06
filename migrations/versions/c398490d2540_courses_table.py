"""courses table

Revision ID: c398490d2540
Revises: 9495d5d8bda3
Create Date: 2018-04-15 21:47:00.781488

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c398490d2540'
down_revision = '9495d5d8bda3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('state', sa.String(length=15), nullable=True))
    op.create_index(op.f('ix_course_state'), 'course', ['state'], unique=False)
    op.drop_index('ix_course_course', table_name='course')
    op.create_index(op.f('ix_course_course'), 'course', ['course'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_course_course'), table_name='course')
    op.create_index('ix_course_course', 'course', ['course'], unique=1)
    op.drop_index(op.f('ix_course_state'), table_name='course')
    op.drop_column('course', 'state')
    # ### end Alembic commands ###
