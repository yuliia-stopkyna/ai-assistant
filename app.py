import uuid

from flask import Flask, request, render_template, make_response

from conversation import get_ai_answer

app = Flask(__name__)


@app.get("/")
def question_page():
    return render_template("question_form.html")


@app.post("/")
def get_answer():
    conversation_id = request.cookies.get("conversation_id", None)
    question = request.form["question"]

    if not conversation_id:
        conversation_id = str(uuid.uuid4())
        is_new = True

    else:
        is_new = False

    answer = get_ai_answer(
        conversation_id=conversation_id, is_new=is_new, question=question
    )

    response = make_response(render_template("answer.html", answer=answer))

    if is_new:
        response.set_cookie("conversation_id", conversation_id)

    return response


if __name__ == "__main__":
    app.run()
