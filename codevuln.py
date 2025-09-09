from flask import Flask, request
import yaml
import os
import requests

app = Flask(__name__)

# Vulnérabilité 1 : Command injection
@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # ⚠️ Ne JAMAIS faire ça
    result = os.popen(f"ping -c 1 {host}").read()
    return f"<pre>{result}</pre>"

# Vulnérabilité 2 : YAML unsafe load
@app.route("/load_yaml", methods=["POST"])
def load_yaml():
    data = request.data.decode("utf-8")
    # ⚠️ Vulnérable à l'exécution de code si l'entrée est malveillante
    parsed = yaml.load(data, Loader=yaml.FullLoader)
    return f"<pre>{parsed}</pre>"

# Vulnérabilité 3 : Redirection non sécurisée
@app.route("/redirect")
def unsafe_redirect():
    url = request.args.get("url", "http://example.com")
    r = requests.get(url)  # ⚠️ Pas de validation d'URL
    return r.text

if __name__ == "__main__":
    app.run(debug=True)
