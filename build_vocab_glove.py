"""Build an np.array from some glove file and some vocab file
You need to download `glove.840B.300d.txt` from
https://nlp.stanford.edu/projects/glove/ and you need to have built
your vocabulary first (Maybe using `build_vocab.py`)
"""

__author__ = "Guillaume Genthial"

from collections import Counter
from pathlib import Path
import numpy as np

def buildVocab(datadir):
    MINCOUNT = 1
    # 1. Words
    # Get Counter of words on all the data, filter by min count, save
    def words(datadir, name):
        return f'{datadir}/{name}_words.txt'

    print('Build vocab words (may take a while)')
    counter_words = Counter()
    for n in ['train', 'test', 'val']:
        with Path(words(datadir, n)).open() as f:
            for line in f:
                counter_words.update(line.strip().split())

    vocab_words = {w for w, c in counter_words.items() if c >= MINCOUNT}

    with Path(f'{datadir}/vocab_words.txt').open('w') as f:
        for w in sorted(list(vocab_words)):
            f.write(f'{w}\n')
    print(f'- done. Kept {len(vocab_words)} out of {len(counter_words)}')

    # 2. Chars
    # Get all the characters from the vocab words
    print('Build vocab chars')
    vocab_chars = set()
    for w in vocab_words:
        vocab_chars.update(w)

    with Path(f'{datadir}/vocab_chars.txt').open('w') as f:
        for c in sorted(list(vocab_chars)):
            f.write(f'{c}\n')
    print(f'- done. Found {len(vocab_chars)} chars')

    # 3. Tags
    # Get all tags from the training set

    def tags(datadir, name):
        return f'{datadir}/{name}_tags.txt'

    print('Build vocab tags (may take a while)')
    vocab_tags = set()
    with Path(tags(datadir, 'train')).open() as f:
        for line in f:
            vocab_tags.update(line.strip().split())

    with Path(f'{datadir}/vocab_tags.txt').open('w') as f:
        for t in sorted(list(vocab_tags)):
            f.write(f'{t}\n')
    print(f'- done. Found {len(vocab_tags)} tags.')


def buildGlove(datadir, glove_txt_path):
    # Load vocab
    with Path(f'{datadir}/vocab_words.txt').open() as f:
        word_to_idx = {line.strip(): idx for idx, line in enumerate(f)}

    size_vocab = len(word_to_idx)

    # Array of zeros
    embeddings = np.zeros((size_vocab, 300))

    # Get relevant glove vectors
    found = 0
    print('Reading GloVe file (may take a while)')
    with Path(glove_txt_path).open() as f:
        for line_idx, line in enumerate(f):
            if line_idx % 100000 == 0:
                print(f'- At line {line_idx}')
            line = line.strip().split()
            if len(line) != 300 + 1:
                continue
            word = line[0].strip()
            embedding = line[1:]
            # if word == "the" or word == "gene":
            #     breakpoint()
            if word in word_to_idx:
            # if word in word_to_idx.keys():
                found += 1
                word_idx = word_to_idx[word]
                # breakpoint()
                embeddings[word_idx] = embedding
    print(f'- done. Found {found} vectors for {size_vocab} words')

    # Save np.array to file
    np.savez_compressed(f"{datadir}/glove.npz", embeddings=embeddings)

