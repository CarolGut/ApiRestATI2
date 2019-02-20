from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

PRODUCTOS = {
    'producto1': {
        "name": "Queso", 
        "price" : 5000
    },
    'producto2': {
        "name": "Pan",
        "price" : 900
    },
    'producto3': {
        "name": "Pizza",
        "price" : 20000
    },
    'producto4': {
        "name": "Chocolate",
        "price" : 3000
    },
    'producto5': {
       "name": "Helado", 
       "price" : 3400
    },
    'producto6': {
        "name": "Galletas",
        "price" : 4000
    },
}


def abort_if_producto_doesnt_exist(producto_id):
    if producto_id not in PRODUCTOS:
        abort(404, message="{} no existe".format(producto_id))

parser = reqparse.RequestParser()
parser.add_argument('name',default=None)
parser.add_argument('price',default=None,type=float)


class Producto(Resource):
    def get(self, producto_id):
        abort_if_producto_doesnt_exist(producto_id)
        return PRODUCTOS[producto_id]

    def delete(self, producto_id):
        abort_if_producto_doesnt_exist(producto_id)
        del PRODUCTOS[producto_id]
        return 'Eliminado con exito!', 200

    def put(self, producto_id):
        args = parser.parse_args()
        if args['name'] is not None:
            PRODUCTOS[producto_id]['name'] = args['name']
        
        if args['price'] is not None:
            PRODUCTOS[producto_id]['price'] = args['price']

        return PRODUCTOS[producto_id], 201


class ProductoList(Resource):
    def get(self):
        return PRODUCTOS

    def post(self):
        args = parser.parse_args()
        producto_id = int(max(PRODUCTOS.keys()).lstrip('producto')) + 1
        producto_id = 'producto%i' % producto_id
        PRODUCTOS[producto_id] = {
            'name': args['name'],
            'price': args['price']
        }
        return PRODUCTOS[producto_id], 201


api.add_resource(ProductoList, '/productos')
api.add_resource(Producto, '/productos/<producto_id>')


if __name__ == '__main__':
    app.run(debug=True)