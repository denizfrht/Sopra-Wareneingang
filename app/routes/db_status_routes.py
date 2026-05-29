from flask import Blueprint, render_template

from app.db import fetch_all


db_status_bp = Blueprint("db_status", __name__)


REQUIRED_VIEWS = [
    ("list_views", "V_LIST_GOODS_RECEIPT"),
    ("list_views", "V_LIST_GOODS_RECEIPT_ITEM"),
    ("list_views", "V_LIST_SUPPLIER_INVOICE"),
    ("list_views", "V_LIST_SUPPLIER_INVOICE_ITEM"),
    ("ins_views", "V_INS_GOODS_RECEIPT"),
    ("ins_views", "V_INS_GOODS_RECEIPT_ITEM"),
    ("ins_views", "V_INS_SUPPLIER_INVOICE"),
    ("upd_views", "V_UPD_GOODS_RECEIPT"),
    ("upd_views", "V_UPD_GOODS_RECEIPT_ITEM"),
    ("upd_views", "V_UPD_SUPPLIER_INVOICE"),
    ("lov_views", "LOV_STATUS_GOODS_RECEIPT"),
    ("lov_views", "LOV_GOODS_CONDITION"),
    ("lov_views", "LOV_STATUS_SUPPLIER_INVOICE"),
]


@db_status_bp.route("/db-status")
def db_status():
    view_status = []

    for schema, view_name in REQUIRED_VIEWS:
        try:
            result = fetch_all("""
                SELECT
                    TABLE_SCHEMA,
                    TABLE_NAME
                FROM INFORMATION_SCHEMA.VIEWS
                WHERE TABLE_SCHEMA = ?
                  AND TABLE_NAME = ?
            """, [schema, view_name])

            exists = len(result) > 0

        except Exception:
            exists = False

        view_status.append({
            "schema": schema,
            "view_name": view_name,
            "exists": exists
        })

    return render_template(
        "db_status.html",
        view_status=view_status
    )