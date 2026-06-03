from flask import Flask, session


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "dev-secret-key"

    @app.context_processor
    def inject_user_role():
        return {
            "current_role": session.get("current_role", "WARENEINGANG")
        }

    from app.routes.goods_receipt_routes import goods_receipt_bp
    from app.routes.supplier_invoice_routes import supplier_invoice_bp

    app.register_blueprint(goods_receipt_bp)
    app.register_blueprint(supplier_invoice_bp)

    return app