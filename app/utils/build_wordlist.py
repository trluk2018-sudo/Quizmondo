"""Build the shared English dictionary the word games check guesses against.

One dictionary, loaded into the Flask process once and held read-only, serves
every word game and every player at the same time. It is deliberately NOT sent
to the browser: at 315,000 words it is 2.9MB of mobile data, so the page keeps
a small common-word list for instant answers and asks the server about
anything it does not recognise.

Source: the dwyl/english-words list (public domain), which carries British
spellings — colour, realise, centre, defence, programme, travelling — as well
as American ones. It is generous on purpose: wrongly rejecting a real word
that a player typed is far more annoying than accepting one they would not
have chosen themselves.

To rebuild:

    curl -L -o words_alpha.txt \\
      https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt
    python -m app.utils.build_wordlist words_alpha.txt

The output is gzipped and committed, because it is slow-changing reference
data and we would rather not depend on a download at deploy time.
"""
import gzip
import os
import sys

MIN_LEN = 3
MAX_LEN = 12


def build(source_path: str, output_path: str) -> int:
    words = set()
    with open(source_path, encoding='utf-8') as fh:
        for line in fh:
            word = line.strip().lower()
            if MIN_LEN <= len(word) <= MAX_LEN and word.isalpha() and word.isascii():
                words.add(word)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    payload = '\n'.join(sorted(words)).encode('utf-8')
    with gzip.open(output_path, 'wb', compresslevel=9) as out:
        out.write(payload)
    return len(words)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    target = os.path.join(root, 'app', 'data', 'words-en.txt.gz')
    total = build(sys.argv[1], target)
    size = os.path.getsize(target) / 1024
    print(f'Wrote {total} words to {target} ({size:.0f} KB gzipped)')
