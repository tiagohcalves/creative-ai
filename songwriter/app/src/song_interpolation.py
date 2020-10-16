import numpy as np


def interpolate(e1, e2, n, w1=0.5, w2=0.5, shuffle=False):
    if shuffle:
        np.random.shuffle(e1)
        np.random.shuffle(e2)

    return (
            (w1 * e1[:n ,:] + w2 * e2[:n ,:]) / (w1+w2)
    )


def interpolate_songs(ae, song_1, song_2, w1, w2, shuffle):
    encoding_s1 = np.load(f"../data/song_sentence_encodings/{song_1}.npz")['arr_0']
    encoding_s2 = np.load(f"../data/song_sentence_encodings/{song_2}.npz")['arr_0']

    n_phrases = min(len(encoding_s1), len(encoding_s2))
    interpolated_enc = interpolate(encoding_s1, encoding_s2, n_phrases, w1, w2, shuffle)
    interpolate_dec = ae.decode(interpolated_enc)

    new_song = '\n'.join(
        [' '.join(p)
            .replace('<unk>', '')
            .replace(' \' ', '\'')
            .replace(' ,', ',')
            .replace(' ?', '?')
            .replace(' !', '!')
            .strip()
            .capitalize()
         for p in interpolate_dec]
    )
    return new_song
