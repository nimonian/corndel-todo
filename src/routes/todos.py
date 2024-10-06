from flask import Blueprint, request, jsonify
from sqlalchemy import text


def todos_bp(db):
    bp = Blueprint("todos", __name__)

    @bp.route("", methods=["POST"])
    def add_todo():
        """
        Add a new todo to the database.

        :param title: The title of the todo item
        :param done: Whether the todo item is done
        :return: The new todo item, serialized as JSON
        :statuscode 201: The todo item was successfully added
        """
        todo = request.get_json()
        query = text("INSERT INTO todos (title, done) VALUES (:title, :done)")
        db.session.execute(query, {"title": todo["title"], "done": todo["done"]})
        db.session.commit()
        return jsonify(todo), 201

    @bp.route("", methods=["GET"])
    def get_todos():
        """
        Get all todos from the database.

        :return: A list of all todos, serialized as JSON
        """
        query = text("SELECT * FROM todos")
        result = db.session.execute(query).fetchall()
        todos = [row._asdict() for row in result]
        return jsonify(todos)

    @bp.route("/<int:id>", methods=["GET"])
    def get_todo(id):
        """
        Get a single todo from the database.

        :param id: The id of the todo item
        :return: The todo item, serialized as JSON
        :statuscode 200: The todo item was found
        :statuscode 404: The todo item was not found
        """
        query = text("SELECT * FROM todos WHERE id=:id")
        result = db.session.execute(query, {"id": id}).fetchone()
        if result:
            return jsonify(result._asdict())
        else:
            return jsonify({"error": "Todo not found"}), 404

    @bp.route("/<int:id>", methods=["DELETE"])
    def delete_todo(id):
        """
        Delete a todo from the database.

        :param id: The id of the todo item
        :return: A JSON object with a success message
        :statuscode 200: The todo item was found and deleted
        :statuscode 404: The todo item was not found
        """
        query = text("DELETE FROM todos WHERE id=:id")
        result = db.session.execute(query, {"id": id})
        db.session.commit()
        if result.rowcount:
            return jsonify({"message": "Todo deleted successfully"}), 200
        else:
            return jsonify({"error": "Todo not found"}), 404

    @bp.route("/todos/<int:id>", methods=["PUT"])
    def update_todo(id):
        """
        Update a todo in the database.

        :param id: The id of the todo item
        :return: The updated todo item, serialized as JSON
        :statuscode 200: The todo item was found and updated
        :statuscode 404: The todo item was not found
        """
        todo = request.get_json()
        query = text("UPDATE todos SET title=:title, done=:done WHERE id=:id")
        result = db.session.execute(
            query, {"title": todo["title"], "done": todo["done"], "id": id}
        )
        db.session.commit()
        if result.rowcount:
            return jsonify(todo)
        else:
            return jsonify({"error": "Todo not found"}), 404

    return bp
