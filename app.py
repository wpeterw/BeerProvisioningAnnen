from flask import Flask
from flask_restplus import Api, Resource, fields

flask_app = Flask(__name__)
app = Api(app=flask_app,
          version="1.0",
          title="BeerProvisioningAnnen",
          description="Get details of beers brewed by BeerProvisioningAnnen")

name_space = app.namespace('BeerProvisioningAnnen', description='Beer API')

model = app.model('Beer Model',
                  {'name': fields.String(required=True,
                                         description="Name of the beer",
                                         help="Name cannot be blank.")})

list_of_beers = {'weizen': {'name': 'Weizen', 'style': 'Hefe weizen',
                            'ingredients': {
                             'malts': 'Pilsener, Muenchener, Wheat',
                             'hops': 'Hallertau',
                             'yeast': 'Gozdawa Bavarian Wheat'},
                            'alcohol': 5.7},
                 'ipa': {'name': 'IPA', 'style': 'Indian Pale Ale',
                         'ingredients': {
                          'malts': 'Pale Ale, Cora',
                          'hops': 'Perle, Cascade',
                          'yeast': 'Gozdawa Old German'},
                         'alcohol': 5.0},
                 }


@name_space.route("/api/v1.0/beer/<name>")
class MainClass(Resource):

    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'name': 'Specify the name of the beer'})
    def get(self, name):
        try:
            beer = list_of_beers[name.lower()]
            return {
                'status': 'Beer retrieved',
                'name': beer['name'],
                'style': beer['style'],
                'ingredients': beer['ingredients'],
                'alcohol': beer['alcohol']
            }
        except KeyError as e:
            name_space.abort(500, e.__doc__, status="Could not retrieve information", statusCode="500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status="Could not retrieve information", statusCode="400")