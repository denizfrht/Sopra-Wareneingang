/*
Benötigte Datenbankobjekte für Modul Gruppe 04:
Wareneingänge aus Lieferungen erstellen und Lieferantenrechnungen erfassen

Stand:
Die Flask-App ist verbunden.
Die folgenden Views/Funktionen müssen noch mit dem Prof geprüft bzw. angelegt werden.
*/


/* ============================================================
   LIST-VIEWS
   ============================================================ */

-- 1. Übersicht Wareneingänge
-- Erwartete Spalten:
-- GOODS_RECEIPT_ID
-- PO_ID
-- SUPPLIER_ID
-- RECEIPT_DATE
-- DELIVERY_NOTE_NO
-- STATUS
-- STATUS_NAME
-- INS_USER
-- INS_DATE
-- UPD_USER
-- UPD_DATE
-- FROM list_views.V_LIST_GOODS_RECEIPT


-- 2. Wareneingangspositionen
-- Erwartete Spalten:
-- GOODS_RECEIPT_ITEM_ID
-- GOODS_RECEIPT_ID
-- PO_ID
-- PO_ITEM_ID
-- ARTICLE / COMPONENT_NAME
-- ORDERED_QTY
-- RECEIVED_QTY
-- CONDITION_ID
-- CONDITION_NAME
-- INS_USER
-- INS_DATE
-- UPD_USER
-- UPD_DATE
-- FROM list_views.V_LIST_GOODS_RECEIPT_ITEM


-- 3. Lieferantenrechnungen
-- Erwartete Spalten:
-- INVOICE_ID
-- GOODS_RECEIPT_ID
-- PO_ID
-- SUPPLIER_ID
-- INVOICE_DATE
-- DUE_DATE
-- TOTAL_NET_AMOUNT
-- TOTAL_VAT_AMOUNT
-- TOTAL_GROSS_AMOUNT
-- INVOICE_STATUS
-- INVOICE_STATUS_NAME
-- INS_USER
-- INS_DATE
-- UPD_USER
-- UPD_DATE
-- FROM list_views.V_LIST_SUPPLIER_INVOICE


-- 4. Lieferantenrechnungspositionen
-- Erwartete Spalten:
-- INVOICE_ITEM_ID
-- INVOICE_ID
-- GOODS_RECEIPT_ITEM_ID
-- NET_AMOUNT
-- VAT_AMOUNT
-- GROSS_AMOUNT
-- FROM list_views.V_LIST_SUPPLIER_INVOICE_ITEM


/* ============================================================
   INSERT-VIEWS
   ============================================================ */

-- ins_views.V_INS_GOODS_RECEIPT
-- Benötigt für: neuen Wareneingang anlegen
-- Eingabefelder:
-- PO_ID
-- RECEIPT_DATE
-- DELIVERY_NOTE_NO
-- STATUS = 200


-- ins_views.V_INS_GOODS_RECEIPT_ITEM
-- Benötigt für: neue Wareneingangsposition anlegen
-- Eingabefelder:
-- GOODS_RECEIPT_ID
-- PO_ITEM_ID
-- ORDERED_QTY
-- RECEIVED_QTY
-- CONDITION_ID


-- ins_views.V_INS_SUPPLIER_INVOICE
-- Benötigt für: neue Lieferantenrechnung anlegen
-- Eingabefelder:
-- GOODS_RECEIPT_ID
-- PO_ID
-- SUPPLIER_ID
-- INVOICE_DATE
-- DUE_DATE
-- TOTAL_NET_AMOUNT
-- TOTAL_VAT_AMOUNT
-- TOTAL_GROSS_AMOUNT
-- INVOICE_STATUS = 300


/* ============================================================
   UPDATE-VIEWS
   ============================================================ */

-- upd_views.V_UPD_GOODS_RECEIPT
-- Benötigt für: Statuswechsel Wareneingang
-- Felder:
-- GOODS_RECEIPT_ID
-- STATUS


-- upd_views.V_UPD_GOODS_RECEIPT_ITEM
-- Benötigt für: Wareneingangsposition bearbeiten
-- Felder:
-- GOODS_RECEIPT_ITEM_ID
-- RECEIVED_QTY
-- CONDITION_ID


-- upd_views.V_UPD_SUPPLIER_INVOICE
-- Benötigt für: Rechnung an Buchhaltung übermitteln
-- Felder:
-- INVOICE_ID
-- INVOICE_STATUS


/* ============================================================
   LOV-VIEWS
   ============================================================ */

-- lov_views.LOV_STATUS_GOODS_RECEIPT
-- 200 ERFASST
-- 201 IN PRUEFUNG
-- 202 WARENEINGANG GEBUCHT
-- 203 MIT ABWEICHUNG
-- 204 IN KLAERUNG
-- 205 RETOURE VERANLASST

-- lov_views.LOV_GOODS_CONDITION
-- 401 BESCHAEDIGT
-- 402 FALSCHLIEFERUNG
-- 404 UNVOLLSTAENDIG
-- 405 UEBERLIEFERUNG
-- 406 KOMBINIERTE ABWEICHUNG
-- 407 WARE OK
-- 408 PRUEFUNG AUSSTEHEND

-- lov_views.LOV_STATUS_SUPPLIER_INVOICE
-- 300 ERFASST
-- 301 AN BUCHHALTUNG UEBERMITTELT