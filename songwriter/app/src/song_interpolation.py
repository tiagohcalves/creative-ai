import numpy as np


def interpolate(e1, e2, n, w1=0.5, w2=0.5, shuffle=False):
    if shuffle:
        np.random.shuffle(e1)
        np.random.shuffle(e2)

    return (
            (w1 * e1[:n ,:] + w2 * e2[:n ,:]) / (w1+w2)
    )


def interpolate_songs(ae, encodings, song_sentence_indexes, song_1, song_2, w1, w2, shuffle):
    song_1_lyrics = song_sentence_indexes[song_1]
    song_2_lyrics = song_sentence_indexes[song_2]

    encoding_s1 = encodings[song_1_lyrics]
    encoding_s2 = encodings[song_2_lyrics]

    n_phrases = min(len(encoding_s1), len(encoding_s2))
    interpolated_enc = interpolate(encoding_s1, encoding_s2, n_phrases, w1, w2, shuffle)
    interpolate_dec = ae.decode(interpolated_enc)

    new_song = '\n'.join([' '.join(p).replace('<unk>', '').strip() for p in interpolate_dec])
    return new_song
