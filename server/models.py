from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    serialize_rules = ("-reviews.customer",)

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'
    
    reviews = db.relationship(
        'Review', back_populates='customer', cascade='all, delete-orphan')
    
    items = association_proxy('reviews', 'item',
                                creator=lambda item_obj: Assignment(item=item_obj))


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    serialize_rules = ("-reviews.item",)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'
    
    reviews = db.relationship(
        'Review', back_populates='item', cascade='all, delete-orphan')
    
    customers = association_proxy('reviews', 'customer',
                                creator=lambda customer_obj: Assignment(customer=customer_obj))

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    serialize_rules = ("-customer.reviews", "-item.reviews")

    # Foreign key to store the employee id
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    # Foreign key to store the project id
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    # Relationship mapping the assignment to related employee
    customer = db.relationship('Customer', back_populates='reviews')
    # Relationship mapping the assignment to related project
    item = db.relationship('Item', back_populates='reviews')
