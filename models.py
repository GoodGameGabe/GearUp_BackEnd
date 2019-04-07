from flask_sqlalchemy import SQLAlchemy
  
db = SQLAlchemy()

#helperTable  

#USER
#BUNDLE
#ARTICLE
#SPEC
#CART

#HELPER TABLE
   
articles_specs = db.Table('articles_specs',
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
    db.Column('spec_id', db.Integer, db.ForeignKey('spec.id'), primary_key=True)
)

articles_bundles = db.Table('articles_bundles',
    db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
    db.Column('bundle_id', db.Integer, db.ForeignKey('bundle.id'), primary_key=True)
)

users_bundles = db.Table('cart',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('bundle_id', db.Integer, db.ForeignKey('bundle.id'), primary_key=True)
)

bundles_items = db.Table('bundles_items',
    db.Column('bundle_id', db.Integer, db.ForeignKey('bundle.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
)

#USER TABLE 
#USER TABLE 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    cart = db.relationship("Bundle", secondary=users_bundles, lazy='subquery',
                        backref=db.backref("users", lazy=True))
    
    def __repr__(self):
        return 'User: %s' % self.username
  
    def to_dict(self):
        cart = []
        for c in self.cart:
            cart.append(c.to_dict())
        return { 
          "id": self.id, 
          "username": self.username, 
          "password": self.password,
          "cart": cart
        }

    def not_dict(self):
        cart = []
        for c in self.cart:
            cart.append(c.id)
        return { 
          "id": self.id, 
          "username": self.username, 
          "password": self.password,
          "cart": cart
        }

#BUNDLE TABLE   
#BUNDLE TABLE        
class Bundle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    tagline = db.Column(db.Text(), unique=False, nullable=False)
    body = db.Column(db.Text(), unique=False, nullable=False)
    picture = db.Column(db.Text(), unique=False, nullable=False)
    vendor = db.Column(db.String(80), unique=False, nullable=False)
    budget = db.Column(db.String(80), unique=False, nullable=False)
    items = db.relationship("Item", secondary=bundles_items, lazy='subquery',
                        backref=db.backref("bundles", lazy=True))
    
    def __repr__(self):
        return 'Bundle: %s' % self.title
  
    def to_dict(self):
        items = []
        for i in self.items:
            items.append(i.to_dict())
        return { 
          "id": self.id, 
          "title": self.title, 
          "tagline": self.tagline,
          "budget": self.budget,
          "picture": self.picture,
          "body": self.body,
          "vendor": self.vendor,
          "items": items
        }
    
    def not_dict(self):
        items = []
        for i in self.items:
            items.append(i.id)
        return { 
          "id": self.id, 
          "title": self.title, 
          "budget": self.budget,
          "tagline": self.tagline,
          "picture": self.picture,
          "body": self.body,
          "vendor": self.vendor,
          "items": items
        }
    
#ARTICLE TABLE         
#ARTICLE TABLE 
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    category = db.Column(db.String(80), unique=False, nullable=False)
    picture = db.Column(db.Text(), unique=False, nullable=False)
    specs = db.relationship("Spec", secondary=articles_specs, lazy='subquery',
                        backref=db.backref("articles", lazy=True))
    bundles = db.relationship("Bundle", secondary=articles_bundles, lazy='subquery',
                        backref=db.backref("articles", lazy=True))
  
    def __repr__(self):
        return 'Article: %s' % self.title
  
    def to_dict(self):
        specs = []
        for s in self.specs:
            specs.append(s.to_dict())
        bundles = []
        for b in self.bundles:
            bundles.append(b.to_dict())
        return { 
          "id": self.id, 
          "title": self.title, 
          "picture": self.picture,
          "category": self.category,
          "specs": specs,
          "bundles": bundles
        }
    
    def not_dict(self):
        specs = []
        for s in self.specs:
            specs.append(s.id)
        bundles = []
        for b in self.bundles:
            bundles.append(b.id)
        return { 
          "id": self.id, 
          "title": self.title, 
          "picture": self.picture,
          "category": self.category,
          "specs": specs,
          "bundles": bundles
        }

#SPEC TABLE            
#SPEC TABLE
class Spec(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    category = db.Column(db.String(80), unique=False, nullable=False)
    body = db.Column(db.Text(), unique=False, nullable=False)
    picture = db.Column(db.Text(), unique=False, nullable=False)
    
    def __repr__(self):
        return 'Spec: %s' % self.title
  
    def not_dict(self):
        return { 
          "id": self.id, 
          "title": self.title, 
          "category": self.category,
          "body": self.body,
          "picture": self.picture
        }
           
#ITEM TABLE
#ITEM TABLE             
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), unique=True, nullable=False)
    price = db.Column(db.String(80), unique=False, nullable=False)
    brand = db.Column(db.String(80), unique=False, nullable=False)
    vendor = db.Column(db.String(80), unique=False, nullable=True)
    category = db.Column(db.String(80), unique=False, nullable=False)
       
    def __repr__(self):
        return 'Item: %s' % self.name
        
    def to_dict(self):
        return { 
          "id": self.id,
          "name": self.name, 
          "price": self.price,
          "brand": self.brand,
          "vendor": self.vendor,
          "category": self.category
        }