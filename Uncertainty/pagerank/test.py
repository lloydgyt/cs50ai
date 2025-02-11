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

def test_transition_model():
    proba_dist = pr.transition_model(CORPORA[4], "1", pr.DAMPING)
    print(proba_dist)

# test_transition_model()