"""create user and related tables

Revision ID: 013f1866bae5
Revises:
Create Date: 2023-07-04 23:16:11.123192

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "013f1866bae5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "address",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("street", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("city", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("state", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("complement", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("zipcode", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user_role",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("role", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("role"),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "hashed_password", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column("first_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("last_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("role", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["role"],
            ["user_role.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_table(
        "customer",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("address_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["address_id"],
            ["address.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_table(
        "employee",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("job_title", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("user_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("employee")
    op.drop_table("customer")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_table("user")
    op.drop_table("user_role")
    op.drop_table("address")
    # ### end Alembic commands ###