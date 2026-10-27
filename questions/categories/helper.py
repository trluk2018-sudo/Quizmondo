# -*- coding: utf-8 -*-
import random

def make_q(prompt, correct, distractors, explanation, difficulty="medium"):
    opts = [correct] + distractors[:3]
    rng = random.Random(prompt)
    rng.shuffle(opts)
    letters = ['A', 'B', 'C', 'D']
    return {
        "prompt": prompt,
        "options": {letters[i]: opts[i] for i in range(4)},
        "correct": letters[opts.index(correct)],
        "explanation": explanation,
        "difficulty": difficulty,
        "type": "classic"
    }
