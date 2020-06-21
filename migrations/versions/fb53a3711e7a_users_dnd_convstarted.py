"""zz

Revision ID: fb53a3711e7a
Revises: d81903c49930
Create Date: 2020-06-20 17:45:37.007793

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "fb53a3711e7a"
down_revision = "d81903c49930"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "conversation_started",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=True,
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "do_not_disturb",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=True,
        ),
    )
    op.drop_column("users", "receive_notifications")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "receive_notifications",
            sa.BOOLEAN(),
            server_default=sa.text("true"),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_column("users", "do_not_disturb")
    op.drop_column("users", "conversation_started")
    # ### end Alembic commands ###