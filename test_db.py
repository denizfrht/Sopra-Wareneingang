from app.db import fetch_all

try:
    result = fetch_all("""
        SELECT
            TABLE_SCHEMA,
            TABLE_NAME
        FROM INFORMATION_SCHEMA.VIEWS
        WHERE TABLE_NAME LIKE '%GOODS%'
           OR TABLE_NAME LIKE '%RECEIPT%'
           OR TABLE_NAME LIKE '%WARE%'
           OR TABLE_NAME LIKE '%INVOICE%'
           OR TABLE_NAME LIKE '%SUPPLIER%'
        ORDER BY TABLE_SCHEMA, TABLE_NAME
    """)

    print("Gefundene Views:")
    for row in result:
        print(row)

except Exception as e:
    print("Fehler beim Suchen der Views:")
    print(e)