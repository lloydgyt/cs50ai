import pagerank as pr

CORPORA = [
    # 0: simple
    {
        "1": {"2"},
        "2": {"1", "3"},
        "3": {"2", "4"},
        "4": {"2"}
    },

    # 1: slightly more involved
    {
        "1": {"2", "3"},
        "2": {"1", "3", "4"},
        "3": {"4", "5"},
        "4": {"1", "2", "3", "6"},
        "5": {"3"},
        "6": {"1", "2", "3"}
    },

    # 2: disjoint
    {
        "1": {"2"},
        "2": {"1", "3"},
        "3": {"2", "4"},
        "4": {"2"},
        "5": {"6"},
        "6": {"5", "7"},
        "7": {"6", "8"},
        "8": {"6"}
    },

    # 3: no links
    {
        "1": {"2"},
        "2": {"1", "3"},
        "3": {"2", "4", "5"},
        "4": {"1", "2"},
        "5": set()
    },

    # 4: test transition model
    {
        "1": {"2", "3"},
        "2": {"3"},
        "3": {"2"},
    }
]

RANKS = [
    # 0: simple
    {
        "1": 0.21991,
        "2": 0.42921,
        "3": 0.21991,
        "4": 0.13096
    },

    # 1: slightly more involved
    {
        "1": 0.12538,
        "2": 0.13922,
        "3": 0.31297,
        "4": 0.19746,
        "5": 0.15801,
        "6": 0.06696
    },

    # 2: disjoint
    {
        "1": 0.10996,
        "2": 0.21461,
        "3": 0.10996,
        "4": 0.06548,
        "5": 0.10996,
        "6": 0.21461,
        "7": 0.10996,
        "8": 0.06548
    },

    # 3: no links
    {
        "1": 0.24178,
        "2": 0.35320,
        "3": 0.19773,
        "4": 0.10364,
        "5": 0.10364
    }
]

# ranks for just corpus 0 with damping factor 0.60
RANK_0_60 = {
    "1": 0.21893,
    "2": 0.39645,
    "3": 0.21893,
    "4": 0.16568
}

def test_transition_model():
    proba_dist = pr.transition_model(CORPORA[4], "1", pr.DAMPING)
    print(proba_dist)

def test_iterate0():
    """iterate_pagerank returns correct results for simple corpus"""
    damping = 0.85
    corpus = CORPORA[0].copy()
    expected = RANKS[0]
    tolerance = 0.002
    actual = pr.iterate_pagerank(corpus, damping)
    print(f"DEBUG: tolerance: {tolerance} - expected: {expected}, get {actual}")

def test_iterate3():
    """iterate_pagerank returns correct results for corpus with pages without links"""
    damping = 0.85
    corpus = CORPORA[3].copy()
    expected = RANKS[3]
    tolerance = 0.002
    actual = pr.iterate_pagerank(corpus, damping)
    print(f"DEBUG: tolerance: {tolerance} - expected: {expected}, get {actual}")

# test_transition_model()
# print(pr.g(CORPORA[3]))
# test_iterate0()
test_iterate3()