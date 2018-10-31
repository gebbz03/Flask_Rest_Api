from flask import Flask, request
from flask_restful import Resource, Api,reqparse
from flask_jwt import JWT,jwt_required
from security import authenticate,identity

app=Flask(__name__)
app.secret_key='gebbz'
api=Api(app)

jwt=JWT(app,authenticate,identity) # /auth

items=[]


#POST
class Item(Resource):

    parser=reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help="This field cannot be left blank!"
        )
   

    
    @jwt_required()
    def get(self,name):
        item=next(filter(lambda x: x['name'] == name,items),None)
        return {'item':None},200 if item else 404     



    def post(self,name):
        #data=request.get_json(silent=True)
        
        if next(filter(lambda x: x['name'] == name,items),None):
            return {'message':"An item with name'{}' already exists.".format(name)},400

        data=Item.parser.parse_args()
        item={'name':name,'price':data['price']}
        items.append(item)
        return item,201    



    #@jwt_required() -- optional any function
    def delete(self,name):
        global items
        items=list(filter(lambda x: x['name'] != name,items))
        return{'message':'Item deleted'}



    def put(self,name):
        data=Item.parser.parse_args()
        item=next(filter(lambda x:x['name'] == name,items),None)
        if item is None:
            item={'name':name,'price':data['price']}
            items.append(item)

        else:
            item.update(data)  

        return item          



class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')



'''
--127.0.0.1:5000/auth
--POST
--HEADERS -- Content-Type -- application/json
--RAW
--{
    "username":"gebbz",
    "password":"gebbz4ever"
}

----------------------------------------
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDA5OTUxOTcsImlhdCI6MTU0MDk5NDg5NywibmJmIjoxNTQwOTk0ODk3LCJpZGVudGl0eSI6MX0.ArGkXGDFJUd5SPTEgNMvsNMHdEKxhl6m0DZrUd-VibE"
}



-----------------
--http://127.0.0.1:5000/item/shoes
--POST
--HEADERS -- Content-Type -- application/json
--RAW
--{
    "price":15:99
}


--http://127.0.0.1:5000/items

--http://127.0.0.1:5000/item/shoes
--GET
--HEADERS -- Authorization -- jwt eyJ0eXAiOiJKV1QiLCJ........


--http://127.0.0.1:5000/item/shoes
--DELETE




--http://127.0.0.1:5000/item/shoes
--PUT
--HEADERS -- Content-Type -- application/json
--RAW
--{
    "price":100
   
}


'''




app.run(port=5000,debug=True)