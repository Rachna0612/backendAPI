from app import db, Incident

incident1 = Incident(title="Incident 1", description="Description of incident 1", severity="Low")
incident2 = Incident(title="Incident 2", description="Description of incident 2", severity="High")

db.session.add_all([incident1, incident2])
db.session.commit()

print("Sample incidents added!")
