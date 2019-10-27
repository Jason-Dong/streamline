import firebase_admin
from firebase_admin import credentials, firestore

def get_val_from_request(request, key):
    request_json = request.get_json()
    if request.args and key in request.args:
        return request.args.get(key)
    elif request_json and key in request_json:
        return request_json[key]

def get_db():
    default_app = firebase_admin.initialize_app()
    return firestore.client()

db = get_db()

def get_doc(collname, docname):
    """
    Returns a reference to the given document in the given collection. If the document doesn't exist, a new one is created.
    """
    return get_collection(collname).document(docname)

def add_doc(collname, docname):
    get_doc(collname, docname).set({'exists':'true'})

def get_collection(name):
    return db.collection(name)

def exists(collname, docname):
    return get_collection(collname).document(docname).get().exists