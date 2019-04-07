import os, copy
import sqlalchemy
from models import db, User, Article, Item, Bundle, Spec
from models import articles_bundles, articles_specs, bundles_items, users_bundles
from flask_migrate import Migrate
from flask import Flask, jsonify, request

app = Flask(__name__)
##Setting the place for the db to run
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/geeaejjdrup.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Initializing the db (after registering the Models)
db.init_app(app)
#migration engine
migrate = Migrate(app, db)

#FUNCTIONS
#getAll
#getID
#deleteID
#updateID
#noresponse

def getAll(table):
    entries = table.query.all()
    arr = []
    for e in entries:
        entry = e.not_dict()
        arr.append(entry)
    
    return arr
    
def getID(anID, table):
    if anID is not None:
        entry = table.query.get(anID)
        return jsonify({"data": entry.to_dict()})

    return no_response()
    
def deleteID(anID, table):
    if id is not None:
        entry = table.query.get(anID)
        arr = []
        arr.append(entry)
        db.session.delete(entry)
        db.session.commit()
        return jsonify({"deleted": "%s" % arr})
    
    return no_response()

def checkRelationship(entity, table, attribute):
    info = request.get_json() or {} 
    if info[attribute] is not None:
        for e in info[attribute]:
            thing = table.query.get(e)
            att = r"attribute"
            if thing is not None:
                entity.att.append(thing)
            else:
                return jsonify("error")
    
def updateID(entityID, table, attributes, 
r_tables, relationships, request):
    if entityID is not None:
        info = request.get_json() or {}    
        entity = table.query.get(entityID) 
        for attribute in attributes:
            a = r"attribute"
            entity.a = info[attribute]

    for relationship in relationships:
        if relationship is not None:
            for r in relationship:
                relation = r_tables.query.get(r)
                if relation is not None:
                    rel = r'relationship'
                    entity.rel.append(relation)
                else:
                    return jsonify("error")
            
        db.session.commit()
        return jsonify({"status_code":"200","data":entity.not_dict()})

    return(no_response())
    
def no_response():
    no_response = jsonify({"error": 400, "message":"no member found" })
    no_response.status_code = 400
    return no_response

@app.route('/', methods=['GET'])
def test(): 
    return ("TEST")
    
@app.route('/users', methods=['GET'])
def getUsers(): 
    return jsonify({"data": getAll(User)})
    
@app.route('/user/<int:id>', methods=['GET','PUT','DELETE'])
def getUserID(id): 
    if id > 0:
        if request.method == 'GET':
            return(getID(id, User))
        elif request.method == 'PUT':
            if id is not None:
                info = request.get_json() or {}    
                user = User.query.get(id) 
                user.username = info["username"]
                user.password = info["password"]
                cart = info["cart"] 
                
                if cart is not None:
                    for cart_bundle in cart:
                        bundle = Bundle.query.get(cart_bundle)
                        if bundle is not None:
                            user.cart.append(bundle)
                        else:
                            return jsonify("error")
                db.session.commit()
                return jsonify({"status_code":"200","data":user.not_dict()})
            else:
                return(no_response())
        elif request.method == 'DELETE':
            return(deleteID(id, User))
        else:
            return("NOTHING")

@app.route('/user/add', methods=['POST'])
def addUser(): 
    info = request.get_json() or {} 
    entity = User(
        username= info["username"],
        password = info["password"]
        )  
    
    attributes = ["cart"]
    for attribute in attributes:
        checkRelationship(entity, User, attribute)

    db.session.add(entity)
    db.session.commit()
    return jsonify({"response":"ok"})

@app.route('/bundles', methods=['GET'])
def getBundles(): 
    return jsonify({"data": getAll(Bundle)})

@app.route('/bundle/<int:id>', methods=['GET','PUT','DELETE'])
def getBundleID(id): 
    if id > 0:
        if request.method == 'GET':
            return(getID(id, Bundle))
        elif request.method == 'PUT':
            if id is not None:
                info = request.get_json() or {}    
                bundle = Bundle.query.get(id) 
                bundle.title = info["title"]
                bundle.tagline = info["tagline"]
                bundle.picture = info["picture"]  
                bundle.vendor = info["vendor"]
                bundle.budget = info["budget"]
                bundle.body = info["body"]
                items = info["items"]
                
                if items is not None:
                    for i in items:
                        item = Item.query.get(i)
                        bundle.items.append(item)
                        
               
                db.session.commit()
                return jsonify({"status_code":"200","data":bundle.to_dict()})
            else:
                return(no_response())
        elif request.method == 'DELETE':
            return(deleteID(id, Bundle))
        else:
            return("Non-Valid Method")

@app.route('/bundle/<int:id>/item/<int:idx>', methods=['DELETE'])
def delBundleItem(id, idx):
    arr = []
    info = request.get_json() or {} 
    bundle = Bundle.query.get(id)
    items = info["items"]
    
    if items is not None:
        item = items[idx]
        if item is not None:
            arr.append(item.to_dict())
            bundle.items.delete(item)
        db.session.commit()
        return jsonify({"deleted": "%s" % arr})
    else:
        return("nope")
        return(no_response())

@app.route('/bundle/add', methods=['POST'])
def addBundle(): 
    info = request.get_json() or {} 
    entity = Bundle(
        title=info["title"],
        tagline = info["tagline"],
        picture=info["picture"],
        vendor = info["vendor"],
        budget=info["budget"],
        body = info["body"]
        )  
    
    checkRelationship(entity, Bundle, "items")

    db.session.add(entity)
    db.session.commit()
    return jsonify({"response":"ok"})   

@app.route('/items', methods=['GET'])
def getItems(): 
    return jsonify({"data": getAll(Item)})

@app.route('/item/<int:id>', methods=['GET','PUT','DELETE'])
def getItemID(id): 
    if id > 0:
        if request.method == 'GET':
            return(getID(id, Item))
        elif request.method == 'PUT':
            if id is not None:
                info = request.get_json() or {}    
                item = Item.query.get(id) 
                item.name = info["name"]
                item.brand = info["brand"]
                item.price = info["price"]
                item.category = info["category"]
                item.vendor = info["vendor"]
                db.session.commit()
                return jsonify({"status_code":"200","data":item.to_dict()})
            else:
                return(no_response())
        elif request.method == 'DELETE':
            return(deleteID(id, Item))
        else:
            return("Non-Valid Method")

@app.route('/item/add', methods=['POST'])
def addItem(): 
    info = request.get_json() or {} 
    entity = Item(
        name=info["name"],
        brand = info["brand"],
        price=info["price"],
        vendor = info["vendor"],
        category=info["category"]
        )  
    db.session.add(entity)
    db.session.commit()
    return jsonify({"response":"ok"}) 

@app.route('/articles', methods=['GET'])
def getArticles(): 
    return jsonify({"data": getAll(Article)})

@app.route('/article/<int:id>', methods=['GET','PUT','DELETE'])
def getArticleID(id): 
    if id > 0:
        if request.method == 'GET':
            return(getID(id, Article))
        elif request.method == 'PUT':
            if id is not None:
                info = request.get_json() or {}    
                article = Article.query.get(id) 
                article.title = info["title"]
                article.category = info["category"]
                article.picture = info["picture"]
                specs = info["specs"] 
                bundles = info["bundles"] 
                
                if specs is not None:
                    for s in specs:
                        spec = Spec.query.get(s)
                        if spec is not None:
                            article.specs.append(spec)
                        else:
                            return jsonify("error")
                            
                if bundles is not None:
                    for b in bundles:
                        bundle = Bundle.query.get(b)
                        if bundle is not None:
                            article.bundles.append(bundle)
                        else:
                            return jsonify("error")
                
                db.session.commit()
                return jsonify({"status_code":"200","data":article.not_dict()})
            else:
                return(no_response())
        elif request.method == 'DELETE':
            return(deleteID(id, Article))
        else:
            return("NOTHING")

@app.route('/article/add', methods=['POST'])
def addArticle(): 
    info = request.get_json() or {} 
    entity = Article(
        title=info["title"],
        category = info["category"],
        picture=info["picture"]
        )  
    
    checkRelationship(entity, Spec, "specs")
    checkRelationship(entity, Bundle, "bundles")

    db.session.add(entity)
    db.session.commit()
    return jsonify({"response":"ok"})   
    
@app.route('/specs', methods=['GET'])
def getSpecs(): 
    return jsonify({"data": getAll(Spec)})

@app.route('/spec/<int:id>', methods=['GET','PUT','DELETE'])
def getSpecID(id): 
    if id > 0:
        if request.method == 'GET':
            return(getID(id, Spec))
        elif request.method == 'PUT':
            if id is not None:
                info = request.get_json() or {}    
                spec = Spec.query.get(id) 
                spec.title = info["title"]
                spec.category = info["category"]
                spec.body = info["body"] 
                spec.picture = info["picture"] 
                db.session.commit()
                return jsonify({"status_code":"200","data":spec.not_dict()})
            else:
                return(no_response())
        elif request.method == 'DELETE':
            return(deleteID(id, Spec))
        else:
            return("NOTHING")

@app.route('/spec/add', methods=['POST'])
def addSpec(): 
    info = request.get_json() or {}
    entity = Spec(
        title = info["title"],
        category = info["category"],
        body = info["body"],
        picture = info["picture"]
        )    
    db.session.add(entity)
    db.session.commit()
    return jsonify({"response":"ok"}) 
    
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))