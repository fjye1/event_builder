from flask import Blueprint, request, jsonify
from app.models import Client, Product, ProductExtra, Staff, EventProduct


api_bp = Blueprint('api', __name__)

@api_bp.route("/api/clients")
def api_clients():
    company_id = request.args.get("company_id", type=int)
    if company_id:
        clients = Client.query.filter_by(company_id=company_id).all()
    else:
        clients = Client.query.all()
    return jsonify([{"id": c.id, "name": c.name} for c in clients])


@api_bp.route("/api/venues")
def api_venues():
    client_id = request.args.get("client_id", type=int)
    if client_id:
        client = Client.query.get(client_id)
        venues = client.venues if client else []
    else:
        venues = []
    return jsonify([{"id": v.id, "name": v.name} for v in venues])


@api_bp.route("/api/staff")
def api_staff():
    staff = Staff.query.filter_by(active=True).all()
    return jsonify([{"id": s.id, "name": s.name} for s in staff])


@api_bp.route("/api/products")
def api_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name} for p in products])


@api_bp.route("/api/extras")
def api_extras():
    product_ids = request.args.getlist("product_id", type=int)
    if not product_ids:
        return jsonify([])
    extras = ProductExtra.query.filter(ProductExtra.product_id.in_(product_ids)).all()
    return jsonify([{"id": e.id, "name": e.name} for e in extras])


@api_bp.route("/api/event_products")
def api_event_products():
    event_id = request.args.get("event_id", type=int)

    if not event_id:
        return jsonify([])

    event_products = EventProduct.query.filter_by(event_id=event_id).all()

    return jsonify([
        {
            "id": ep.id,
            "label": f"{ep.product.name} ({ep.start_time} - {ep.end_time})"
        }
        for ep in event_products
    ])