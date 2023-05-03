"""Flask app for Cupcakes"""
from flask import Flask, render_template, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'hey'
app.debug = True

toolbar = DebugToolbarExtension(app)

connect_db(app)
# with app.app_context():
#     db.create_all()

@app.route("/")
def home():
    """Display home page."""

    return render_template("index.html")

@app.route("/api/cupcakes")
def get_cupcake():
    """List all cupcakes."""

    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Create new cupcake."""

    data = request.json

    cupcake = Cupcake(
        flavor = data["flavor"],
        rating=data["rating"],
        size=data["size"],
        image=data["image"] or None)

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()), 201)

@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    """Get cupcake with specified id."""

    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    """Update fields on specified cupcake."""

    data = request.json

    cupcake = Cupcake.query.get_or_404(id)


    cupcake.flavor = data["flavor"],
    cupcake.rating=data["rating"]
    cupcake.size=data["size"]
    cupcake.image=data["image"]
    

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    """Delete specified cupcake."""

    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(messsage="Deleted")