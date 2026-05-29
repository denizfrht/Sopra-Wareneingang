def get_goods_conditions():
    """
    Liefert alle Condition-Werte für Wareneingangspositionen.
    Später kommen diese Werte aus lov_views.LOV_GOODS_CONDITION.
    """

    return [
        {"CONDITION_ID": 401, "CONDITION_NAME": "BESCHAEDIGT"},
        {"CONDITION_ID": 402, "CONDITION_NAME": "FALSCHLIEFERUNG"},
        {"CONDITION_ID": 404, "CONDITION_NAME": "UNVOLLSTAENDIG"},
        {"CONDITION_ID": 405, "CONDITION_NAME": "UEBERLIEFERUNG"},
        {"CONDITION_ID": 406, "CONDITION_NAME": "KOMBINIERTE ABWEICHUNG"},
        {"CONDITION_ID": 407, "CONDITION_NAME": "WARE OK"},
        {"CONDITION_ID": 408, "CONDITION_NAME": "PRUEFUNG AUSSTEHEND"},
    ]


def get_condition_name(condition_id):
    """
    Gibt zur CONDITION_ID den passenden Namen zurück.
    """

    for condition in get_goods_conditions():
        if condition["CONDITION_ID"] == int(condition_id):
            return condition["CONDITION_NAME"]

    return "UNBEKANNT"


def suggest_condition_id(ordered_qty, received_qty, damaged=False, wrong_delivery=False):
    """
    Schlägt anhand von bestellter und gelieferter Menge eine CONDITION_ID vor.

    Fachliche Logik:
    - beschädigt + Mengenabweichung = kombinierte Abweichung
    - beschädigt = beschädigt
    - falsche Lieferung = Falschlieferung
    - weniger geliefert = unvollständig
    - mehr geliefert = Überlieferung
    - exakt geliefert = Ware OK
    """

    ordered_qty = float(ordered_qty)
    received_qty = float(received_qty)

    if damaged and received_qty != ordered_qty:
        return 406

    if damaged:
        return 401

    if wrong_delivery:
        return 402

    if received_qty < ordered_qty:
        return 404

    if received_qty > ordered_qty:
        return 405

    if received_qty == ordered_qty:
        return 407

    return 408