import os
from pathlib import Path

import click
from fastai.learner import load_learner


from quest_generator import __version__


def load_model():
    """Load model from file."""
    path = Path(os.path.realpath(__file__)).resolve().parent.parent.parent
    path = path/"assets/model.pkl"
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



@click.command()
@click.version_option(version=__version__)
def main():
    click.echo(
        """
           ____                  _      _____                           _             
          / __ \                | |    / ____|                         | |            
         | |  | |_   _  ___  ___| |_  | |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ __ 
         | |  | | | | |/ _ \/ __| __| | | |_ |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
         | |__| | |_| |  __/\__ \ |_  | |__| |  __/ | | |  __/ | | (_| | || (_) | |   
          \___\_\\__,_|\___||___/\__|  \_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|   
        """,
        color="green"
    )

    model = load_model()
    quest_goals = []

    quest_title = click.prompt('Enter the quest title')

    click.echo(quest_title)

    while True:
        click.echo("-------------------------------------------------------")
        suggestions = get_next_suggestions(model, quest_title, quest_goals)
        for i, s in enumerate(suggestions):
            click.echo(f"{i} -> {s}")

        next_goal = click.prompt("Select next goal", type=int)
        quest_goals.append(suggestions[next_goal])

        click.echo("\n")
        click.echo(quest_title)
        click.echo("\n".join(quest_goals))


if __name__ == '__main__':
    main()
