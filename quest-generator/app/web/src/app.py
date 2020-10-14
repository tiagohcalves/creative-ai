import os
import json
import sys
from pathlib import Path

import flask
import yaml
from fastai.learner import load_learner
from flask import Flask

with open("src/config.yaml", 'r') as stream:
    APP_CONFIG = yaml.full_load(stream)

app = Flask(__name__)


def load_model():
    """Load model from file."""
    path = Path(os.path.realpath(__file__)).resolve().parent.parent
    path = path/"models/model.pkl"
    learner = load_learner(path, cpu=False)
    return learner


def get_next_suggestions(model, quest_title, quest_goals, n_preds=5, n_words=15):
    """Get the next goal suggestions from the model, given the current context"""
    if quest_goals:
        context = quest_title.lower() + " > " + " > ".join(quest_goals).lower() + " > "
    else:
        context = quest_title.lower() + " > "
    predictions = []

    for _ in range(n_preds):
        prediction = model.predict(context, n_words)[len(context):]
        predictions += [
            p.strip()
            for p in prediction.split(">")
            if len(p) > 0
        ]

    # TODO replace placeholders

    return predictions


@app.route('/api/update_quest', methods=['POST'])
def update_quest():
    request_data = json.loads(flask.request.data)
    quest_title = request_data.get("title")
    selected_suggestion = request_data.get("selected")
    quest_goals = request_data.get("quest_goals")

    if selected_suggestion:
        quest_goals.append(selected_suggestion)

    current_suggestions = get_next_suggestions(model, quest_title, quest_goals)
    res = {
        "title": quest_title,
        "current_goals": quest_goals,
        "suggestions": current_suggestions
    }

    return flask.jsonify(res)


@app.route('/ping', methods=['GET'])
def ping():
    return "pong"


@app.route('/config')
def config():
    return flask.jsonify(APP_CONFIG)


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"

    response.cache_control.max_age = 0
    return response


@app.route('/<path:path>')
def static_file(path):
    if ".js" in path or ".css" in path:
        return app.send_static_file(path)
    else:
        return app.send_static_file('index.html')


@app.route('/')
def root():
    return app.send_static_file('index.html')


def before_request():
    app.jinja_env.cache = {}


model = load_model()

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)

    if "prepare" not in sys.argv:
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        # app.run(debug=False, host='0.0.0.0', port=port)
        app.run(host='0.0.0.0', port=port)
