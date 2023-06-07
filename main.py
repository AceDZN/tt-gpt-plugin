import json
import requests

import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

@app.get("/hello/<string:name>")
async def sayHello(name):
    return quart.Response(response=f"Hello {name}!", status=200, mimetype="text/json")

@app.get("/tinytap-games/<string:category>")
async def get_games(category):
    r = requests.get("https://staging.tinytap.it/store/api/content/search/{category}?language=all&ageGroup=all&include_courses=1&ver=3.5&page_num=1&per_page=20")
    d = r.json()
    
    games = d['data']
    print(games)
    return quart.Response(response=json.dumps(games), status=200, mimetype="text/json")

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
