"""inicial: usuarios, proveedores, facturas, bitacora, reportes

Revision ID: 0001
Revises:
Create Date: 2026-06-18

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(120), nullable=False),
        sa.Column("email", sa.String(150), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("rol", sa.String(30), nullable=False, server_default="operador"),
        sa.Column("creado_en", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_usuarios_email", "usuarios", ["email"], unique=True)

    op.create_table(
        "proveedores",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(150), nullable=False),
        sa.Column("nit", sa.String(30), nullable=False),
        sa.Column("direccion", sa.String(255), nullable=True),
        sa.Column("telefono", sa.String(30), nullable=True),
        sa.Column("email", sa.String(150), nullable=True),
        sa.Column("creado_en", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_proveedores_nit", "proveedores", ["nit"], unique=True)

    op.create_table(
        "facturas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre_archivo", sa.String(255), nullable=False),
        sa.Column("numero_factura", sa.String(50), nullable=True),
        sa.Column("fecha", sa.Date(), nullable=True),
        sa.Column("subtotal", sa.Numeric(12, 2), nullable=True),
        sa.Column("impuestos", sa.Numeric(12, 2), nullable=True),
        sa.Column("total", sa.Numeric(12, 2), nullable=True),
        sa.Column("texto_ocr", sa.Text(), nullable=True),
        sa.Column("estado", sa.String(20), nullable=False, server_default="pendiente"),
        sa.Column("proveedor_id", sa.Integer(), sa.ForeignKey("proveedores.id"), nullable=True),
        sa.Column("usuario_id", sa.Integer(), sa.ForeignKey("usuarios.id"), nullable=True),
        sa.Column("creado_en", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "bitacora",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("factura_id", sa.Integer(), sa.ForeignKey("facturas.id"), nullable=True),
        sa.Column("usuario_id", sa.Integer(), sa.ForeignKey("usuarios.id"), nullable=True),
        sa.Column("tipo_evento", sa.String(20), nullable=False),
        sa.Column("documento", sa.String(255), nullable=True),
        sa.Column("estado", sa.String(20), nullable=False),
        sa.Column("resultado", sa.Text(), nullable=True),
        sa.Column("fecha_hora", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "reportes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("usuario_id", sa.Integer(), sa.ForeignKey("usuarios.id"), nullable=True),
        sa.Column("formato", sa.String(10), nullable=False),
        sa.Column("filtros", sa.Text(), nullable=True),
        sa.Column("fecha_generacion", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("reportes")
    op.drop_table("bitacora")
    op.drop_table("facturas")
    op.drop_index("ix_proveedores_nit", table_name="proveedores")
    op.drop_table("proveedores")
    op.drop_index("ix_usuarios_email", table_name="usuarios")
    op.drop_table("usuarios")
