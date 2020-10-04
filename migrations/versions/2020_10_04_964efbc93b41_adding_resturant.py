"""adding resturant

Revision ID: 964efbc93b41
Revises:
Create Date: 2020-10-04 13:23:15.659651

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "964efbc93b41"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "restaurant",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "insert_datetime",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("address", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("cuisine", sa.String(), nullable=False),
        sa.Column("price", sa.String(), nullable=False),
        sa.Column("menu_url", sa.String(), nullable=True),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_restaurant_id"), "restaurant", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_restaurant_insert_datetime"),
        "restaurant",
        ["insert_datetime"],
        unique=False,
    )
    op.create_index(
        op.f("ix_restaurant_name"), "restaurant", ["name"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_restaurant_name"), table_name="restaurant")
    op.drop_index(
        op.f("ix_restaurant_insert_datetime"), table_name="restaurant"
    )
    op.drop_index(op.f("ix_restaurant_id"), table_name="restaurant")
    op.drop_table("restaurant")
    # ### end Alembic commands ###