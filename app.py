from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///incident.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Incident model
class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(10), nullable=False)
    reported_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "reported_at": self.reported_at.isoformat()
        }

# Initialize the database
with app.app_context():
    db.create_all()

# Route: GET /incidents (Fetch all incidents)
@app.route('/incidents', methods=['GET'])
def get_all_incidents():
    incidents = Incident.query.all()
    return jsonify([incident.to_dict() for incident in incidents]), 200

# Route: POST /incidents (Add a new incident)
@app.route('/incidents', methods=['POST'])
def add_incident():
    data = request.get_json()

    # Validation
    if not data or not all(k in data for k in ('title', 'description', 'severity')):
        return jsonify({"error": "Missing required fields"}), 400

    if data['severity'] not in ['Low', 'Medium', 'High']:
        return jsonify({"error": "Severity must be 'Low', 'Medium', or 'High'"}), 400

    new_incident = Incident(
        title=data['title'],
        description=data['description'],
        severity=data['severity']
    )
    db.session.add(new_incident)
    db.session.commit()

    return jsonify(new_incident.to_dict()), 201

# Route: GET /incidents/<id> (Fetch a single incident by ID)
@app.route('/incidents/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    incident = Incident.query.get(incident_id)
    if not incident:
        return jsonify({"error": "Incident not found"}), 404

    return jsonify(incident.to_dict()), 200

# Route: DELETE /incidents/<id> (Delete an incident)
@app.route('/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    incident = Incident.query.get(incident_id)
    if not incident:
        return jsonify({"error": "Incident not found"}), 404

    db.session.delete(incident)
    db.session.commit()

    return jsonify({"message": f"Incident {incident_id} deleted successfully."}), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
