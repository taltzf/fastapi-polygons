from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '5e2d0e3eea73'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'polygons',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('points', sa.String, nullable=False),  # storing JSON as string
    )


def downgrade() -> None:
    op.drop_table('polygons')
