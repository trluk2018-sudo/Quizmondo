# -*- coding: utf-8 -*-
"""Merge question categories into app/data/mega_questions_3000.json.

Why this exists alongside scratch/compile_and_seed_3300.py: that script rebuilds
*every* category from its source module and writes the whole bank out. Several of
the older source modules have drifted smaller than what is committed (match-flags
is 250 questions in the bank but 221 in its module), so running it replaces live
categories with shorter versions and silently loses questions.

This compiler only ever touches the categories listed in OWNED below. Everything
else in the bank is copied through untouched, and it refuses to shrink a category
it does own, so regenerating can add questions but never drop them.

Usage:  python questions/compile_bank.py          (writes the bank)
        python questions/compile_bank.py --check   (reports, writes nothing)
"""
import io
import json
import os
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BANK = os.path.join(REPO, 'app', 'data', 'mega_questions_3000.json')

sys.path.insert(0, REPO)

# Full-size categories this compiler owns, with the metadata the seeder needs
OWNED = {
    'uk-british': {
        'module': 'questions.categories.cat_uk_british',
        'title': 'UK & British Trivia',
        'icon': '\U0001F1EC\U0001F1E7',
        'description': 'Monarchy, Parliament, counties and coastlines, telly and radio, British bands, '
                       'the pub, sport, writers, slang and the inventions that came out of these islands.',
        'minimum': 200,
    },
}

# Categories that already exist in the database and are only being topped up.
# They merge by prompt, so these add to whatever is already there.
OWNED_TOPUPS = {
    'world-history': {
        'title': 'World Trivia',
        'icon': '\U0001F30D',
        'description': 'General knowledge and world history, from the pyramids and the Silk Road to the space race.',
    },
    'science-cosmos': {
        'title': 'Science & Cosmos',
        'icon': '\U0001F52C',
        'description': 'Planets, physics, chemistry and the human body, for the opening round of a quiz night.',
    },
    'gaming-esports': {
        'title': 'Gaming & Esports',
        'icon': '\U0001F3AE',
        'description': 'Arcade classics, consoles, open worlds and the competitive scene.',
    },
}
TOPUP_MODULE = 'questions.categories.cat_thin_topup'
TOPUP_MINIMUM = 30


def shape(items):
    out = []
    for q in items:
        out.append({
            'prompt': q['prompt'],
            'options': q['options'],
            'correct': q['correct'],
            'explanation': q['explanation'],
            'difficulty': q.get('difficulty', 'medium'),
            'type': q.get('type', 'classic'),
            'points': 100,
            'time_limit': 15,
        })
    return out


def load_bank():
    if not os.path.exists(BANK):
        return {'categories': {}}
    return json.load(io.open(BANK, encoding='utf-8'))


def compile_bank(check_only=False):
    bank = load_bank()
    bank.setdefault('categories', {})
    before = {slug: len(cat['questions']) for slug, cat in bank['categories'].items()}

    built = {}

    for slug, meta in OWNED.items():
        module = __import__(meta['module'], fromlist=['get_questions'])
        items = module.get_questions()
        if len(items) < meta['minimum']:
            raise SystemExit(f"{slug} has {len(items)} questions, below its floor of {meta['minimum']}")
        built[slug] = (meta, shape(items))

    topups = __import__(TOPUP_MODULE, fromlist=['TOPUPS']).TOPUPS
    for slug, meta in OWNED_TOPUPS.items():
        if slug not in topups:
            raise SystemExit(f"{slug} is owned here but the top-up module has nothing for it")
        items = topups[slug]()
        if len(items) < TOPUP_MINIMUM:
            raise SystemExit(f"top-up {slug} has {len(items)} questions, below its floor of {TOPUP_MINIMUM}")
        built[slug] = (meta, shape(items))

    problems = []
    for slug, (meta, items) in built.items():
        prompts = [q['prompt'] for q in items]
        if len(prompts) != len(set(prompts)):
            problems.append(f"{slug}: duplicate prompts")
        for q in items:
            if len(set(q['options'].values())) != 4 or q['correct'] not in q['options']:
                problems.append(f"{slug}: malformed question {q['prompt'][:50]!r}")
        # Never let a regeneration shrink a category below what is already committed
        if slug in before and len(items) < before[slug]:
            problems.append(f"{slug}: would shrink from {before[slug]} to {len(items)} questions")
    if problems:
        for p in problems:
            print('PROBLEM', p)
        raise SystemExit('refusing to write the bank')

    print('%-20s %8s %8s' % ('category', 'before', 'after'))
    for slug, (meta, items) in sorted(built.items()):
        print('%-20s %8s %8d' % (slug, before.get(slug, '-'), len(items)))
        if check_only:
            continue
        bank['categories'][slug] = {
            'title': meta['title'],
            'icon': meta['icon'],
            'description': meta['description'],
            'question_count': len(items),
            'questions': items,
        }

    untouched = sorted(set(bank['categories']) - set(built))
    print(f"\n{len(untouched)} other categories left exactly as they are")

    if check_only:
        print('\n--check given: nothing written')
        return bank

    bank['total_categories'] = len(bank['categories'])
    bank['total_questions'] = sum(len(c['questions']) for c in bank['categories'].values())
    bank['generated_at'] = datetime.utcnow().isoformat()
    with io.open(BANK, 'w', encoding='utf-8') as f:
        json.dump(bank, f, ensure_ascii=False, indent=2)
    print(f"\nwrote {bank['total_questions']} questions across {bank['total_categories']} categories")
    return bank


if __name__ == '__main__':
    compile_bank(check_only='--check' in sys.argv)
