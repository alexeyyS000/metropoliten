"""revision

Revision ID: b4c0fcfb55eb
Revises:
Create Date: 2023-07-17 23:14:20.627051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b4c0fcfb55eb"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.Column("publication_date", sa.DateTime(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=True),
        sa.Column("updated", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("posts")
    # ### end Alembic commands ###