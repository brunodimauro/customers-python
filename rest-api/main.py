from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd

app = Flask(__name__)
api = Api(app)
file = r'C:\Users\bruno.dimauro\python\src\sample\rest-api\customers.csv'

class Customer(Resource):
    def get(self):
        data = pd.read_csv(file)
        data = data.to_dict()
        return {'data': data}, 200
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('CustomerId', required=True)
        parser.add_argument('FirstName', required=True)
        parser.add_argument('LastName', required=True)

        args = parser.parse_args()

        new_data = pd.DataFrame({
            'CustomerId': args['CustomerId'],
            'FirstName': args['FirstName'],
            'LastName': args['LastName'],
            'Address': {}
        })
        data = pd.read_csv(file)
        data = data.append(new_data, ignore_index=True)
        data.to_csv(file, index=False)
        return {'data': 'Test' }, 200
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('CustomerId', required=True)
        args = parser.parse_args()

        data = pd.read_csv(file)

        if args['CustomerId'] in list(data['CustomerId']):
            
            user_data = data[data['CustomerId'] == args['CustomerId']]
            user_data["FirstName"] = args["FirstName"]
            user_data["LastName"] = args["LastName"]

            data.to_csv(file, index=False)

            return {'data': data.to_dict()}, 200

        else:
            return {
                'message': f"'{args['CustomerId']}' customer not found."
            }, 404
    pass

#api.add_resource(Customer, '/customer')
api.add_resource(Customer)

if __name__ == '__main__':
    app.run()