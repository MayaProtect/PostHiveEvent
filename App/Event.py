from flask import Flask, request, jsonify, Response

app = Flask(__name__)

class Event:

@app.route('/event', methods=['GET'])
@cross_origin()
def register():
    events = mongo.db.event.find()
    response = json_util.dumps(events)
    return  Response(response, mimetypes='application/json')


@app.route('/event/<id>', methods=['DELETE'])
def delete_event(id)


@app.route('/event/<id>', methods=['PUT'])
def update_event(id):
    eventType = request.json['eventType']
    description = request.json['description']

    if eventType and description:
        mongo.db.event.update_one({'_id': Event(id)}, {$set: {
            'eventType': eventType,
            'description': description
        }})
        response = jsonify({eventType + ' and ' + description + ' was updated successfully' })
        return response



if __name__ == '__main__':
	app.run(debug=True)