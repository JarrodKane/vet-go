"""create_pet_model-2

Revision ID: 0d7ee2cb139a
Revises: 1d189aa56085
Create Date: 2024-01-24 09:29:33.393530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0d7ee2cb139a"
down_revision = "1d189aa56085"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "animal", "phone_number", existing_type=sa.VARCHAR(length=20), nullable=True
    )
    op.alter_column(
        "clinic", "phone_number", existing_type=sa.VARCHAR(length=20), nullable=True
    )
    op.alter_column(
        "organization",
        "phone_number",
        existing_type=sa.VARCHAR(length=20),
        nullable=True,
    )
    op.alter_column(
        "staff", "phone_number", existing_type=sa.VARCHAR(length=20), nullable=True
    )
    op.alter_column(
        "user_model", "phone_number", existing_type=sa.VARCHAR(length=20), nullable=True
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user_model",
        "phone_number",
        existing_type=sa.VARCHAR(length=20),
        nullable=False,
    )
    op.alter_column(
        "staff", "phone_number", existing_type=sa.VARCHAR(length=20), nullable=False
    )
    op.alter_column(
        "organization",
        "phone_number",
        existing_type=sa.VARCHAR(length=20),
        nullable=False,
    )
    op.alter_column(
        "clinic", "phone_number", existing_type=sa.VARCHAR(length=20), nullable=False
    )
    op.alter_column(
        "animal", "phone_number", existing_type=sa.VARCHAR(length=20), nullable=False
    )
    # ### end Alembic commands ###