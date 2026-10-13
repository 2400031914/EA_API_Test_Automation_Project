from flask import Flask, jsonify, request

def create_app():
    app = Flask(__name__)
    users = {
        1: {"id": 1, "name": "Asha", "email": "asha@example.com"},
        2: {"id": 2, "name": "Ravi", "email": "ravi@example.com"},
    }

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @app.get("/users/<int:user_id>")
    def get_user(user_id):
        user = users.get(user_id)
        if user is None:
            return jsonify({"error": "user_not_found"}), 404
        return jsonify(user), 200

    @app.post("/users")
    def create_user():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "invalid_json"}), 400
        name = payload.get("name")
        email = payload.get("email")
        if not isinstance(name, str) or not name.strip():
            return jsonify({"error": "name_required"}), 400
        if not isinstance(email, str) or "@" not in email or "." not in email.split("@")[-1]:
            return jsonify({"error": "invalid_email"}), 400
        new_id = max(users.keys(), default=0) + 1
        user = {"id": new_id, "name": name.strip(), "email": email}
        users[new_id] = user
        return jsonify(user), 201

    return app

if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)
