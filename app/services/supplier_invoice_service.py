from datetime import date
from app.db import fetch_all, fetch_one, execute_query
from app.services.goods_receipt_service import get_goods_receipt_by_id


# Dummy-Daten für Lieferantenrechnungen.
# Später: SELECT aus list_views.V_LIST_SUPPLIER_INVOICE.
supplier_invoices = [
    {
        "INVOICE_ID": 3001,
        "GOODS_RECEIPT_ID": 1001,
        "PO_ID": 5001,
        "SUPPLIER_ID": 7001,
        "INVOICE_DATE": "2026-05-29",
        "DUE_DATE": "2026-06-12",
        "TOTAL_NET_AMOUNT": "1000.00",
        "TOTAL_VAT_AMOUNT": "190.00",
        "TOTAL_GROSS_AMOUNT": "1190.00",
        "INVOICE_STATUS": 300,
        "INVOICE_STATUS_NAME": "ERFASST",
    },
    {
        "INVOICE_ID": 3002,
        "GOODS_RECEIPT_ID": 1002,
        "PO_ID": 5002,
        "SUPPLIER_ID": 7002,
        "INVOICE_DATE": "2026-05-28",
        "DUE_DATE": "2026-06-11",
        "TOTAL_NET_AMOUNT": "2500.00",
        "TOTAL_VAT_AMOUNT": "475.00",
        "TOTAL_GROSS_AMOUNT": "2975.00",
        "INVOICE_STATUS": 301,
        "INVOICE_STATUS_NAME": "AN BUCHHALTUNG UEBERMITTELT",
    },
]


def get_all_supplier_invoices():
    """
    Liefert alle Lieferantenrechnungen.

    Aktuell:
    - versucht echte Daten aus list_views.V_LIST_SUPPLIER_INVOICE zu laden
    - falls die View noch nicht existiert, werden Dummy-Daten verwendet

    Später:
    - sobald die View mit dem Prof angelegt wurde, kommt die Liste automatisch aus der DB
    """

    query = """
        SELECT
            INVOICE_ID,
            GOODS_RECEIPT_ID,
            PO_ID,
            SUPPLIER_ID,
            INVOICE_DATE,
            DUE_DATE,
            TOTAL_NET_AMOUNT,
            TOTAL_VAT_AMOUNT,
            TOTAL_GROSS_AMOUNT,
            INVOICE_STATUS,
            INVOICE_STATUS_NAME
        FROM list_views.V_LIST_SUPPLIER_INVOICE
        ORDER BY INVOICE_ID DESC
    """

    try:
        return fetch_all(query)

    except Exception as e:
        print("DB-View für Lieferantenrechnungen noch nicht verfügbar:")
        print(e)
        print("Es werden Dummy-Daten verwendet.")

        return supplier_invoices


def create_supplier_invoice(
    goods_receipt_id,
    invoice_date,
    due_date,
    total_net_amount,
    total_vat_amount,
    total_gross_amount
):
    """
    Erstellt eine neue Lieferantenrechnung.
    Aktuell Dummy-Daten.
    Später: INSERT über ins_views.V_INS_SUPPLIER_INVOICE.

    Fachliche Regeln:
    - Eine Lieferantenrechnung referenziert genau einen Wareneingang.
    - Wareneingang muss existieren.
    - PO_ID und SUPPLIER_ID werden aus dem Wareneingang übernommen.
    - Rechnungsdatum darf nicht in der Zukunft liegen.
    - Fälligkeitsdatum muss nach dem Rechnungsdatum liegen.
    - Startstatus ist 300 ERFASST.
    """

    goods_receipt = get_goods_receipt_by_id(goods_receipt_id)

    if goods_receipt is None:
        return False, "Der ausgewählte Wareneingang existiert nicht."

    if invoice_date > str(date.today()):
        return False, "Das Rechnungsdatum darf nicht in der Zukunft liegen."

    if due_date <= invoice_date:
        return False, "Das Fälligkeitsdatum muss nach dem Rechnungsdatum liegen."
    
    net = float(total_net_amount)
    vat = float(total_vat_amount)
    gross = float(total_gross_amount)

    if round(net + vat, 2) != round(gross, 2):
        return False, "Der Brutto-Betrag muss Netto-Betrag plus Umsatzsteuerbetrag entsprechen."

    new_id = max(invoice["INVOICE_ID"] for invoice in supplier_invoices) + 1

    new_invoice = {
        "INVOICE_ID": new_id,
        "GOODS_RECEIPT_ID": int(goods_receipt_id),
        "PO_ID": goods_receipt["PO_ID"],
        "SUPPLIER_ID": goods_receipt["SUPPLIER_ID"],
        "INVOICE_DATE": invoice_date,
        "DUE_DATE": due_date,
        "TOTAL_NET_AMOUNT": total_net_amount,
        "TOTAL_VAT_AMOUNT": total_vat_amount,
        "TOTAL_GROSS_AMOUNT": total_gross_amount,
        "INVOICE_STATUS": 300,
        "INVOICE_STATUS_NAME": "ERFASST",
    }

    supplier_invoices.append(new_invoice)

    return True, "Lieferantenrechnung wurde erfolgreich angelegt."


def transmit_supplier_invoice(invoice_id):
    """
    Setzt eine Lieferantenrechnung auf AN BUCHHALTUNG UEBERMITTELT.

    Erlaubter Statusfluss:
    300 ERFASST -> 301 AN BUCHHALTUNG UEBERMITTELT
    """

    for invoice in supplier_invoices:
        if invoice["INVOICE_ID"] == int(invoice_id):

            if invoice["INVOICE_STATUS"] != 300:
                return False, "Diese Rechnung wurde bereits übermittelt oder kann nicht mehr geändert werden."

            invoice["INVOICE_STATUS"] = 301
            invoice["INVOICE_STATUS_NAME"] = "AN BUCHHALTUNG UEBERMITTELT"

            return True, "Lieferantenrechnung wurde an die Buchhaltung übermittelt."

    return False, "Lieferantenrechnung wurde nicht gefunden."