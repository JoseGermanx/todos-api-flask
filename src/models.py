from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(200))
    done = db.Column(db.Boolean)

    def __repr__(self):
        return '<Todo %r>' % self.label
    
    def serialize(self):
        return {
            "id": self.id,
            "label": self.label,
            "done": self.done
        }
    
    def serialize_list(self):
        return {
            "label": self.label,
            "done": self.done
        }
    
    def serialize_update(self):
        return {
            "label": self.label,
            "done": self.done
        }
    
    def serialize_delete(self):
        return {
            "label": self.label,
            "done": self.done
        }
    
    def serialize_add(self):
        return {
            "label": self.label,
            "done": self.done
        }
    
    def serialize_index(self):
        return {
            "label": self.label,
            "done": self.done
        }