# Songwriter / Song Vector Space

App: http://song-vector-space.herokuapp.com/

An analsys of song lyrics using deep learning. It may also be capable of generating new lyrics from the existing ones.

Originally this was a project to generate new lyrics given an artist. The first models did not work so well, so I decided manipulate the lyrics with embeddings and explore the space it creates.

## Built on top of
- [The text-autoencoder developed in the paper "Educating Text Autoencoders: Latent Representation Guidance via Denoising"](https://github.com/shentianxiao/text-autoencoders)
- [This wonderful tutorial](https://reshamas.github.io/deploying-deep-learning-models-on-web-and-mobile/)

## Structure

This respository contains the code to:
- Scrap [https://www.vagalume.com.br/] for lyrics.
- Some of the data used
- Train the autoencoder
- Build song vectors and create the vector space
- Web application with deploy to Heroku using Docker and Dash.
