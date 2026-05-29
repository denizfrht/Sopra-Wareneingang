from datetime import date

from app.db import fetch_all, fetch_one, execute_query
from app.services.purchase_order_service import get_purchase_order_by_id
from app.services.condition_service import get_condition_name, suggest_condition_id

# Dummy-Daten als Liste.
# Später wird diese Liste durch echte Datenbankabfragen ersetzt.
goods_receipts = [
    {
        "GOODS_RECEIPT_ID": 1001,
        "PO_ID": 5001,
        "SUPPLIER_ID": 7001,
        "RECEIPT_DATE": "2026-05-29",
        "DELIVERY_NOTE_NO": "LS-2026-001",
        "STATUS": 200,
        "STATUS_NAME": "ERFASST",
    },
    {
        "GOODS_RECEIPT_ID": 1002,
        "PO_ID": 5002,
        "SUPPLIER_ID": 7002,
        "RECEIPT_DATE": "2026-05-28",
        "DELIVERY_NOTE_NO": "LS-2026-002",
        "STATUS": 201,
        "STATUS_NAME": "IN PRUEFUNG",
    },
]


def get_all_goods_receipts():
    """
    Liefert alle Wareneingänge.

    Aktuell:
    - versucht echte Daten aus list_views.V_LIST_GOODS_RECEIPT zu laden
    - falls die View noch nicht existiert, werden Dummy-Daten verwendet

    Später:
    - sobald die View mit dem Prof angelegt wurde, kommt die Liste automatisch aus der DB
    """

    query = """
        SELECT
            GOODS_RECEIPT_ID,
            PO_ID,
            SUPPLIER_ID,
            RECEIPT_DATE,
            DELIVERY_NOTE_NO,
            STATUS,
            STATUS_NAME
        FROM list_views.V_LIST_GOODS_RECEIPT
        ORDER BY GOODS_RECEIPT_ID DESC
    """

    try:
        return fetch_all(query)

    except Exception as e:
        print("DB-View für Wareneingänge noch nicht verfügbar:")
        print(e)
        print("Es werden Dummy-Daten verwendet.")

        return goods_receipts


def create_goods_receipt(po_id, receipt_date, delivery_note_no):
    """
    Erstellt einen neuen Wareneingang.
    Aktuell nur in Dummy-Daten.
    Später: INSERT über ins_views.V_INS_GOODS_RECEIPT.

    Fachliche Regeln:
    - Bestellung muss vorhanden sein.
    - Wareneingangsdatum darf nicht in der Zukunft liegen.
    - Startstatus ist immer 200 ERFASST.
    """

    po = get_purchase_order_by_id(po_id)

    if po is None:
        return False, "Die ausgewählte Bestellung existiert nicht."

    if receipt_date > str(date.today()):
        return False, "Das Wareneingangsdatum darf nicht in der Zukunft liegen."

    new_id = max(gr["GOODS_RECEIPT_ID"] for gr in goods_receipts) + 1

    new_goods_receipt = {
        "GOODS_RECEIPT_ID": new_id,
        "PO_ID": int(po_id),
        "SUPPLIER_ID": po["SUPPLIER_ID"],
        "RECEIPT_DATE": receipt_date,
        "DELIVERY_NOTE_NO": delivery_note_no,
        "STATUS": 200,
        "STATUS_NAME": "ERFASST",
    }

    goods_receipts.append(new_goods_receipt)

    return True, "Wareneingang wurde erfolgreich angelegt."

from app.services.condition_service import get_condition_name, suggest_condition_id


# Dummy-Daten für Wareneingangspositionen.
# Später: SELECT aus list_views.V_LIST_GOODS_RECEIPT_ITEM.
goods_receipt_items = [
    {
        "GOODS_RECEIPT_ITEM_ID": 9001,
        "GOODS_RECEIPT_ID": 1001,
        "PO_ID": 5001,
        "PO_ITEM_ID": 8001,
        "ARTICLE": "Schraube M8",
        "ORDERED_QTY": 100,
        "RECEIVED_QTY": 100,
        "CONDITION_ID": 407,
        "CONDITION_NAME": "WARE OK",
    },
    {
        "GOODS_RECEIPT_ITEM_ID": 9002,
        "GOODS_RECEIPT_ID": 1002,
        "PO_ID": 5002,
        "PO_ITEM_ID": 8002,
        "ARTICLE": "Metallplatte",
        "ORDERED_QTY": 50,
        "RECEIVED_QTY": 45,
        "CONDITION_ID": 404,
        "CONDITION_NAME": "UNVOLLSTAENDIG",
    },
]


def get_goods_receipt_by_id(goods_receipt_id):
    """
    Sucht einen Wareneingang anhand der GOODS_RECEIPT_ID.
    """

    for gr in goods_receipts:
        if gr["GOODS_RECEIPT_ID"] == int(goods_receipt_id):
            return gr

    return None


def get_items_by_goods_receipt_id(goods_receipt_id):
    """
    Liefert alle Positionen zu einem Wareneingang.
    Später: SELECT aus list_views.V_LIST_GOODS_RECEIPT_ITEM.
    """

    return [
        item for item in goods_receipt_items
        if item["GOODS_RECEIPT_ID"] == int(goods_receipt_id)
    ]


def create_goods_receipt_item(
    goods_receipt_id,
    po_item_id,
    article,
    ordered_qty,
    received_qty,
    condition_id=None,
    damaged=False,
    wrong_delivery=False
):
    """
    Erstellt eine neue Wareneingangsposition.
    Aktuell Dummy-Daten.
    Später: INSERT über ins_views.V_INS_GOODS_RECEIPT_ITEM.

    Wenn keine CONDITION_ID manuell gesetzt wird,
    schlägt das System automatisch eine passende CONDITION_ID vor.
    """

    goods_receipt = get_goods_receipt_by_id(goods_receipt_id)

    if goods_receipt is None:
        return False, "Der ausgewählte Wareneingang existiert nicht."

    if float(ordered_qty) <= 0:
        return False, "Die bestellte Menge muss größer als 0 sein."

    if float(received_qty) < 0:
        return False, "Die gelieferte Menge darf nicht negativ sein."

    if not condition_id:
        condition_id = suggest_condition_id(
        ordered_qty=ordered_qty,
        received_qty=received_qty,
        damaged=damaged,
        wrong_delivery=wrong_delivery
    )

    condition_id = int(condition_id)

    new_id = max(item["GOODS_RECEIPT_ITEM_ID"] for item in goods_receipt_items) + 1

    new_item = {
        "GOODS_RECEIPT_ITEM_ID": new_id,
        "GOODS_RECEIPT_ID": int(goods_receipt_id),
        "PO_ID": goods_receipt["PO_ID"],
        "PO_ITEM_ID": int(po_item_id),
        "ARTICLE": article,
        "ORDERED_QTY": float(ordered_qty),
        "RECEIVED_QTY": float(received_qty),
        "CONDITION_ID": condition_id,
        "CONDITION_NAME": get_condition_name(condition_id),
    }

    goods_receipt_items.append(new_item)

    return True, "Wareneingangsposition wurde erfolgreich angelegt."

def all_items_are_ok(goods_receipt_id):
    """
    Prüft, ob alle Positionen eines Wareneingangs CONDITION_ID = 407 haben.

    Fachliche Regel:
    Ein Wareneingang darf direkt gebucht werden, wenn alle Positionen WARE OK sind.
    """

    items = get_items_by_goods_receipt_id(goods_receipt_id)

    if len(items) == 0:
        return False

    for item in items:
        if item["CONDITION_ID"] != 407:
            return False

    return True


def has_any_deviation(goods_receipt_id):
    """
    Prüft, ob mindestens eine Position eine Abweichung hat.

    Alles ungleich 407 wird hier als Abweichung/offene Prüfung gewertet.
    """

    items = get_items_by_goods_receipt_id(goods_receipt_id)

    for item in items:
        if item["CONDITION_ID"] != 407:
            return True

    return False


def update_goods_receipt_status(goods_receipt_id, target_status):
    """
    Ändert den Status eines Wareneingangs nach erlaubter Statuslogik.

    Später:
    UPDATE über upd_views.V_UPD_GOODS_RECEIPT
    und bei Buchung Bestandsaktualisierung über stored_func.fn_g04_update_component_stock.
    """

    goods_receipt = get_goods_receipt_by_id(goods_receipt_id)

    if goods_receipt is None:
        return False, "Wareneingang wurde nicht gefunden."

    current_status = goods_receipt["STATUS"]
    target_status = int(target_status)

    status_names = {
        200: "ERFASST",
        201: "IN PRUEFUNG",
        202: "WARENEINGANG GEBUCHT",
        203: "MIT ABWEICHUNG",
        204: "IN KLAERUNG",
        205: "RETOURE VERANLASST",
    }

    allowed_transitions = {
        200: [201],
        201: [202, 203],
        203: [204],
        204: [202, 205],
    }

    if current_status not in allowed_transitions:
        return False, "Für den aktuellen Status ist kein weiterer Statuswechsel erlaubt."

    if target_status not in allowed_transitions[current_status]:
        return False, "Dieser Statuswechsel ist fachlich nicht erlaubt."

    # Fachregel: Direktes Buchen aus IN PRUEFUNG nur, wenn alle Positionen WARE OK sind
    if current_status == 201 and target_status == 202:
        if not all_items_are_ok(goods_receipt_id):
            return False, "Direktes Buchen ist nur möglich, wenn alle Positionen CONDITION_ID 407 WARE OK haben."

    # Fachregel: Abweichung dokumentieren nur, wenn es mindestens eine Abweichung gibt
    if current_status == 201 and target_status == 203:
        if not has_any_deviation(goods_receipt_id):
            return False, "Abweichung dokumentieren ist nur möglich, wenn mindestens eine Position eine Abweichung hat."

    goods_receipt["STATUS"] = target_status
    goods_receipt["STATUS_NAME"] = status_names[target_status]

    if target_status == 202:
        return True, "Wareneingang wurde gebucht. Später wird hier die Bestandsaktualisierung angestoßen."

    if target_status == 205:
        return True, "Retoure wurde veranlasst. Es erfolgt kein Lagerzugang."

    return True, f"Status wurde auf {status_names[target_status]} gesetzt."