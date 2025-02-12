import heredity as hd
import math

FAMILIES = [

    # 0: simple
    {
        "Harry": {"name": "Harry", "mother": "Lily", "father": "James", "trait": None},
        "James": {"name": "James", "mother": None, "father": None, "trait": None},
        "Lily": {"name": "Lily", "mother": None, "father": None, "trait": None}
    },

    # 1: multiple children
    {
        "Arthur": {"name": "Arthur", "mother": None, "father": None, "trait": None},
        "Charlie": {"name": "Charlie", "mother": "Molly", "father": "Arthur", "trait": None},
        "Fred": {"name": "Fred", "mother": "Molly", "father": "Arthur", "trait": None},
        "Ginny": {"name": "Ginny", "mother": "Molly", "father": "Arthur", "trait": None},
        "Molly": {"name": "Molly", "mother": None, "father": None, "trait": None},
        "Ron": {"name": "Ron", "mother": "Molly", "father": "Arthur", "trait": None}
    },

    # 2: multiple generations
    {
        "Arthur": {"name": "Arthur", "mother": None, "father": None, "trait": None},
        "Hermione": {"name": "Hermione", "mother": None, "father": None, "trait": None},
        "Molly": {"name": "Molly", "mother": None, "father": None, "trait": None},
        "Ron": {"name": "Ron", "mother": "Molly", "father": "Arthur", "trait": None},
        "Rose": {"name": "Rose", "mother": "Ron", "father": "Hermione", "trait": None}
    }
]

def test__h():
    assert math.isclose(hd._h("James", 0, assumed_condition), 0.01, rel_tol=1e-6)
    assert math.isclose(hd._h("James", 1, assumed_condition), 0.99, rel_tol=1e-6)
    assert math.isclose(hd._h("Lily", 0, assumed_condition), 0.99, rel_tol=1e-6)
    assert math.isclose(hd._h("Lily", 1, assumed_condition), 0.01, rel_tol=1e-6)

def test__f():
    assert math.isclose(hd._f("James", assumed_condition), 0.0065, rel_tol=1e-6)
    assert math.isclose(hd._f("Harry", assumed_condition), 0.431288, rel_tol=1e-6)
    assert math.isclose(hd._f("Lily", assumed_condition), 0.9504, rel_tol=1e-6)

people = FAMILIES[0]
assumed_condition = hd._g(people, {"Harry"}, {"James"}, {"James"})

print(f"{assumed_condition}")