# #!/usr/bin/env python
# import os

# from flask import Flask
# from pymongo import MongoClient

# app = Flask(__name__)

# client = MongoClient("mongo:27017")

# @app.route('/')
# def todo():
#     try:
#         client.admin.command('ismaster')
#     except:
#         return "Server not available"
#     return "Hello from the MongoDB client!\n"


# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)

#!/usr/bin/env python
import os

from flask import Flask, request, render_template
from bson import ObjectId
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongo:27017")
db = client["mydatabase"]
collection = db["people"]

@app.route('/', methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        if request.form.get('action') == 'add':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            collection.insert_one({'first_name': first_name, 'last_name': last_name})
        elif request.form.get('action') == 'delete':
            id_to_delete = request.form.get('id')
            collection.delete_one({'_id': ObjectId(id_to_delete)})
        elif request.form.get('action') == 'edit':
            id_to_edit = request.form.get('id')
            updated_first_name = request.form.get('first_name')
            updated_last_name = request.form.get('last_name')
            collection.update_one({'_id': ObjectId(id_to_edit)}, {'$set': {'first_name': updated_first_name, 'last_name': updated_last_name}})
    
    people = collection.find()
    return render_template('index.html', people=people)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)




