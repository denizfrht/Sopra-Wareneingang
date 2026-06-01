from flask import Flask, session
from app.routes.db_status_routes import db_status_bp

def create_app():
    app = Flask(__name__)

    # Wird später z. B. für Flash-Meldungen/Formulare gebraucht
    app.config["SECRET_KEY"] = "dev-secret-key"
    @app.context_processor
    def inject_user_role():
        return {
            "current_role": session.get("current_role", "WARENEINGANG")
        }

    # Routen importieren
    from app.routes.goods_receipt_routes import goods_receipt_bp
    from app.routes.supplier_invoice_routes import supplier_invoice_bp

    # Routen registrieren
    app.register_blueprint(goods_receipt_bp)
    app.register_blueprint(supplier_invoice_bp)
    app.register_blueprint(db_status_bp)

    return app