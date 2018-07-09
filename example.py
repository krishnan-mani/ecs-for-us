from flask_api import FlaskAPI

app = FlaskAPI(__name__)

@app.route('/example/')
def example():
    return {'hello': 'world', 'workshop': 'ecs', 'bump': 'yes', 'okayed_by_Kostas': 'false'}

if __name__ == "__main__":
        app.run(debug=True,host='0.0.0.0')
