
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os

load_dotenv()

app = Flask(__name__)

# MongoDB connection
mongo_uri = os.getenv("MONGODB_URI")
collection = None

if mongo_uri:
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
        client.admin.command("ping")
        db = client["todo_database"]
        collection = db["todo_items"]
    except Exception as error:
        print("MongoDB connection failed:", error)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api():
    with open("data.json", "r") as file:
        data = json.load(file)
    return jsonify(data)


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = request.form.get("itemName")
    item_description = request.form.get("itemDescription")

    if not item_name or not item_description:
        return jsonify({"error": "Both fields are required"}), 400

    todo = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    if collection is None:
        return jsonify({"error": "MongoDB is not connected"}), 503

    result = collection.insert_one(todo)

    return jsonify({
        "message": "To-Do item saved successfully",
        "id": str(result.inserted_id)
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
