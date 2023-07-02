"""add_user

Revision ID: 93cc7f203901
Revises: 
Create Date: 2023-07-02 23:35:05.789351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "93cc7f203901"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
