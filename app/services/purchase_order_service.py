def get_purchase_orders():
    """
    Liefert auswählbare Bestellungen.
    Aktuell Dummy-Daten.
    Später kommen diese Daten aus der Datenbank, z. B. aus einer Bestell-View.
    """

    return [
        {
            "PO_ID": 5001,
            "SUPPLIER_ID": 7001,
            "SUPPLIER_NAME": "Müller Komponenten GmbH",
            "ORDER_DATE": "2026-05-20",
            "STATUS": "OFFEN",
        },
        {
            "PO_ID": 5002,
            "SUPPLIER_ID": 7002,
            "SUPPLIER_NAME": "Schneider Metallteile AG",
            "ORDER_DATE": "2026-05-21",
            "STATUS": "OFFEN",
        },
        {
            "PO_ID": 5003,
            "SUPPLIER_ID": 7003,
            "SUPPLIER_NAME": "Keller Bauteile GmbH",
            "ORDER_DATE": "2026-05-22",
            "STATUS": "TEILWEISE GELIEFERT",
        },
    ]


def get_purchase_order_by_id(po_id):
    """
    Sucht eine Bestellung anhand der PO_ID.
    Wird gebraucht, damit wir beim Wareneingang automatisch den Lieferanten übernehmen können.
    """

    purchase_orders = get_purchase_orders()

    for po in purchase_orders:
        if po["PO_ID"] == int(po_id):
            return po

    return None

def get_purchase_order_items_by_po_id(po_id):
    """
    Liefert Bestellpositionen zu einer Bestellung.
    Aktuell Dummy-Daten.

    Später:
    Diese Daten kommen aus der echten Bestellpositions-View der Datenbank.
    """

    purchase_order_items = [
        {
            "PO_ID": 5001,
            "PO_ITEM_ID": 8001,
            "ARTICLE": "Schraube M8",
            "ORDERED_QTY": 100,
        },
        {
            "PO_ID": 5001,
            "PO_ITEM_ID": 8004,
            "ARTICLE": "Mutter M8",
            "ORDERED_QTY": 100,
        },
        {
            "PO_ID": 5002,
            "PO_ITEM_ID": 8002,
            "ARTICLE": "Metallplatte",
            "ORDERED_QTY": 50,
        },
        {
            "PO_ID": 5003,
            "PO_ITEM_ID": 8003,
            "ARTICLE": "Gehäusebauteil",
            "ORDERED_QTY": 25,
        },
    ]

    return [
        item for item in purchase_order_items
        if item["PO_ID"] == int(po_id)
    ]