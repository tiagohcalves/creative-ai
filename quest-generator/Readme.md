# Quest Generator

App: https://creative-ai.herokuapp.com/

A deep learning model to iteractively generate quests for adventure games.

## Built on top of
- [fast-ai](https://github.com/fastai)
- [gpt-2](https://huggingface.co/gpt2)
- [This wonderful tutorial](https://reshamas.github.io/deploying-deep-learning-models-on-web-and-mobile/)

## Structure

This respository contains the code to:
- Scrap Fandom for quests of [Skyrim](https://elderscrolls.fandom.com/wiki/Skyrim) and [The Witcher 3](https://witcher.fandom.com/wiki/The_Witcher_3:_Wild_Hunt)
- Some of the data used
- Train the language model from a pre-trained one
- Extract entities from the data (so we generate generic quests, instead of using names and locations from the games)
- Console application
- Web application with deploy to Heroku using Docker and Flask.
