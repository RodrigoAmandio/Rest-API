from sql_alchemy import usage_database

class UsageModel(usage_database.Model):
    __tablename__ = 'usage'
    item_id = usage_database.Column(usage_database.Integer,primary_key=True)
    name = usage_database.Column(usage_database.String(80))
    data = usage_database.Column(usage_database.String(20))
    value = usage_database.Column(usage_database.Float)

    def __init__(self, item_id, name, data, value):
        self.item_id = item_id
        self.name = name
        self.data = data
        self.value = value

    def json(self):
        return {
            'item_id': self.item_id,
            'name': self.name,
            'data': self.data,
            'value': self.value
        }

    @classmethod
    def find_item(cls, item_id):
        item = cls.query.filter_by(item_id=item_id).first()
        # O construtor acima significa: SELECT * FROM usage WHERE item_id = item_id LIMIT = 1
        if item:
            return item
        return None

    def save_item(self):
        usage_database.session.add(self)
        usage_database.session.commit()

    def update_item(self,name, data, value):
        self.name = name
        self.data = data
        self.value = value

    def delete_item(self):
        usage_database.session.delete(self)
        usage_database.session.commit()
