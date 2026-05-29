from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.services.supplier_invoice_service import (
    get_all_supplier_invoices,
    create_supplier_invoice,
    transmit_supplier_invoice,
)
from app.services.goods_receipt_service import get_all_goods_receipts

supplier_invoice_bp = Blueprint("supplier_invoice", __name__)


@supplier_invoice_bp.route("/lieferantenrechnung", methods=["GET", "POST"])
def supplier_invoices():
    if request.method == "POST":
        goods_receipt_id = request.form.get("goods_receipt_id")
        invoice_date = request.form.get("invoice_date")
        due_date = request.form.get("due_date")
        total_net_amount = request.form.get("total_net_amount")
        total_vat_amount = request.form.get("total_vat_amount")
        total_gross_amount = request.form.get("total_gross_amount")

        success, message = create_supplier_invoice(
            goods_receipt_id=goods_receipt_id,
            invoice_date=invoice_date,
            due_date=due_date,
            total_net_amount=total_net_amount,
            total_vat_amount=total_vat_amount,
            total_gross_amount=total_gross_amount
        )

        flash(message, "success" if success else "error")

        return redirect(url_for("supplier_invoice.supplier_invoices"))

    return render_template(
        "supplier_invoices.html",
        supplier_invoices=get_all_supplier_invoices(),
        goods_receipts=get_all_goods_receipts()
    )


@supplier_invoice_bp.route("/lieferantenrechnung/<invoice_id>/uebermitteln", methods=["POST"])
def transmit_invoice(invoice_id):
    success, message = transmit_supplier_invoice(invoice_id)

    flash(message, "success" if success else "error")

    return redirect(url_for("supplier_invoice.supplier_invoices"))