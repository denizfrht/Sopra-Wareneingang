from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from app.services.goods_receipt_service import (
    get_all_goods_receipts,
    create_goods_receipt,
    get_goods_receipt_by_id,
    get_items_by_goods_receipt_id,
    create_goods_receipt_item,
    update_goods_receipt_status,
    ensure_goods_receipt_items_exist,
    update_goods_receipt_item,
)
from app.services.purchase_order_service import get_purchase_orders
from app.services.condition_service import get_goods_conditions, suggest_condition_id

goods_receipt_bp = Blueprint("goods_receipt", __name__)


@goods_receipt_bp.route("/")
def index():
    return redirect(url_for("goods_receipt.goods_receipts"))


@goods_receipt_bp.route("/wareneingang", methods=["GET", "POST"])
def goods_receipts():
    if request.method == "POST":
        po_id = request.form.get("po_id")
        receipt_date = request.form.get("receipt_date")
        delivery_note_no = request.form.get("delivery_note_no")

        success, message = create_goods_receipt(
            po_id=po_id,
            receipt_date=receipt_date,
            delivery_note_no=delivery_note_no
        )

        flash(message, "success" if success else "error")
        return redirect(url_for("goods_receipt.goods_receipts"))

    return render_template(
        "goods_receipts.html",
        goods_receipts=get_all_goods_receipts(),
        purchase_orders=get_purchase_orders()
    )


@goods_receipt_bp.route("/wareneingang/<goods_receipt_id>")
def goods_receipt_detail(goods_receipt_id):
    goods_receipt = get_goods_receipt_by_id(goods_receipt_id)

    if goods_receipt is None:
        flash("Wareneingang wurde nicht gefunden.", "error")
        return redirect(url_for("goods_receipt.goods_receipts"))

    success, message = ensure_goods_receipt_items_exist(goods_receipt_id)

    if not success:
        flash(message, "error")

    items = get_items_by_goods_receipt_id(goods_receipt_id)
    conditions = get_goods_conditions()

    return render_template(
        "goods_receipts.html",
        goods_receipts=get_all_goods_receipts(),
        purchase_orders=get_purchase_orders(),
        selected_goods_receipt=goods_receipt,
        goods_receipt_items=items,
        conditions=conditions
    )


@goods_receipt_bp.route("/wareneingang/<goods_receipt_id>/position", methods=["POST"])
def add_goods_receipt_item(goods_receipt_id):
    po_item_id = request.form.get("po_item_id")
    article = request.form.get("article")
    ordered_qty = request.form.get("ordered_qty")
    received_qty = request.form.get("received_qty")
    condition_id = request.form.get("condition_id")
    damaged = request.form.get("damaged") == "on"
    wrong_delivery = request.form.get("wrong_delivery") == "on"

    success, message = create_goods_receipt_item(
    goods_receipt_id=goods_receipt_id,
    po_item_id=po_item_id,
    article=article,
    ordered_qty=ordered_qty,
    received_qty=received_qty,
    condition_id=condition_id,
    damaged=damaged,
    wrong_delivery=wrong_delivery
)

    flash(message, "success" if success else "error")

    return redirect(
        url_for(
            "goods_receipt.goods_receipt_detail",
            goods_receipt_id=goods_receipt_id
        )
    )

@goods_receipt_bp.route("/wareneingang/<goods_receipt_id>/status", methods=["POST"])
def change_goods_receipt_status(goods_receipt_id):
    target_status = request.form.get("target_status")

    success, message = update_goods_receipt_status(
        goods_receipt_id=goods_receipt_id,
        target_status=target_status
    )

    flash(message, "success" if success else "error")

    return redirect(
        url_for(
            "goods_receipt.goods_receipt_detail",
            goods_receipt_id=goods_receipt_id
        )
    )

@goods_receipt_bp.route("/rolle-wechseln", methods=["POST"])
def change_role():
    """
    Einfacher Rollenwechsel für den Prototyp.

    Für jede Rolle gibt es ein eigenes Passwort.
    Nur wenn Rolle und Passwort zusammenpassen, wird die Rolle in der Session gespeichert.

    Später könnte das durch ein echtes Login-/Rechtesystem ersetzt werden.
    """

    role = request.form.get("role")
    password = request.form.get("password")

    role_passwords = {
        "WARENEINGANG": "we123",
        "BUCHHALTUNG": "buch123",
        "ADMIN": "admin123",
    }

    if role not in role_passwords:
        flash("Ungültige Rolle.", "error")
        return redirect(request.referrer or url_for("goods_receipt.goods_receipts"))

    if password != role_passwords[role]:
        flash("Falsches Passwort für diese Rolle.", "error")
        return redirect(request.referrer or url_for("goods_receipt.goods_receipts"))

    session["current_role"] = role
    flash(f"Rolle wurde auf {role} gesetzt.", "success")

    return redirect(request.referrer or url_for("goods_receipt.goods_receipts"))

@goods_receipt_bp.route("/wareneingang/position/<goods_receipt_item_id>/edit", methods=["POST"])
def edit_goods_receipt_item(goods_receipt_item_id):
    goods_receipt_id = request.form.get("goods_receipt_id")
    received_qty = request.form.get("received_qty")
    condition_id = request.form.get("condition_id")
    damaged = request.form.get("damaged") == "on"
    wrong_delivery = request.form.get("wrong_delivery") == "on"

    success, message = update_goods_receipt_item(
        goods_receipt_item_id=goods_receipt_item_id,
        received_qty=received_qty,
        condition_id=condition_id,
        damaged=damaged,
        wrong_delivery=wrong_delivery
    )

    flash(message, "success" if success else "error")

    return redirect(
        url_for(
            "goods_receipt.goods_receipt_detail",
            goods_receipt_id=goods_receipt_id
        )
    )