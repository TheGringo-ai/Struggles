

from flask import Flask, request, jsonify, redirect, make_response
from flask_cors import CORS
import streamlit.web.bootstrap

app = Flask(__name__)
CORS(app)

@app.route("/token", methods=["POST"])
def receive_token():
    data = request.get_json()
    token = data.get("token")
    if not token:
        return jsonify({"error": "Missing token"}), 400

    # Save token in a cookie or pass it to Streamlit (optional example here)
    resp = make_response(redirect("/"))
    resp.set_cookie("id_token", token)
    return resp

if __name__ == "__main__":
    import threading
    def run_streamlit():
        streamlit.web.bootstrap.run("/Users/fredtaylor/Projects/Struggles/home.py", "", [], {})

    threading.Thread(target=run_streamlit).start()
    app.run(host="0.0.0.0", port=8081)