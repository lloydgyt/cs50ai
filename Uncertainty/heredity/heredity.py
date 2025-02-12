import csv
import itertools
import sys
import math

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people # iterate through the keys
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # sorts the type of problem each person is interested in
    # _g()

    # TODO calculate no parent first? or recursion?
    proba = list()
    # for each person in people, calculate
    # TODO use _g() to refractor
    assumed_condition = _g(people, one_gene, two_genes, have_trait)
    for person in people:
        if person in one_gene:
            num_genes = 1
        elif person in two_genes:
            num_genes = 2
        else:
            num_genes = 0
        if person in have_trait:
            trait = True
        else:
            trait = False
        # TODO will there be single parent?
        has_parent = True if people[person]["mother"] is not None else False
        proba.append(_f(person, assumed_condition))
        # everyone needs to be calculated! so find out who belongs to which

    # multiply every proba together
    return math.prod(proba)

# TODO rename
# TODO why use people here?
def _f(person, assumed_condition):
    """
    return the probability PERSON has based in the interested settings
    """
    # TODO using recursion, may include redundant computation if parents have more than 1 child
    # TODO the type below should be in the arguments
    # have parent or not?
        # if has parent, knowing their parent will help
    # there are 6 types
        # have 0, 1, 2 genes
        # yes, no trait
    has_parent = assumed_condition[person]["has_parent"]
    num_genes = assumed_condition[person]["num_genes"]
    trait = assumed_condition[person]["trait"]
    if not has_parent:
        # unconditional proba
        # TODO don't you need to consider their trait? 
        # seems like the project designer didn't consider
        probability = PROBS["gene"][num_genes] * PROBS["trait"][num_genes][trait]
    else:
        # conditional probability based on parents
        # get their parents assumed condition
        # TODO must be able to get assumed condition from somewhere
        # calculate father contribute 0 or 1 genes
        father = assumed_condition[person]["father"]
        f_0 = _h(father, 0, assumed_condition)
        f_1 = _h(father, 1, assumed_condition)
        # calculate mother contribute 0 or 1 genes
        mother = assumed_condition[person]["mother"]
        m_0 = _h(mother, 0, assumed_condition)
        m_1 = _h(mother, 1, assumed_condition)

        if num_genes == 0:
            probability_genes = f_0 * m_0
        elif num_genes == 1:
            probability_genes = f_1 * m_0 + f_0 * m_1
        elif num_genes == 2: 
            probability_genes = f_1 * m_1

        # compute probability of trait
        probability = probability_genes * PROBS["trait"][num_genes][trait]
    return probability
        

# TODO rename
def _g(people, one_gene, two_genes, have_trait):
    """ return a dictionary containing all assumed condition for everyone """
    assumed_condition = dict()
    for person in people:
        # TODO refactor later! using dict comprehension?
        if person in one_gene:
            num_genes = 1
        elif person in two_genes:
            num_genes = 2
        else:
            num_genes = 0
        if person in have_trait:
            trait = True
        else:
            trait = False
        # TODO will there be single parent?
        has_parent = True if people[person]["mother"] is not None else False
        assumed_condition[person] = {
            "num_genes":num_genes,
            "trait":trait,
            "has_parent":has_parent,
            "mother": people[person]["mother"],
            "father": people[person]["father"]
        }
    return assumed_condition

# TODO rename
def _h(person, num, assumed_condition):
    """ 
    Return the probability that PERSON pass down NUM genes
    to their child

    Assuming that mutation happens after passing the genes
    """
    assert num == 0 or num == 1
    # calculate probability when passing 0 genes
    if assumed_condition[person]["num_genes"] == 0:
        p = 1 - PROBS["mutation"]
    elif assumed_condition[person]["num_genes"] == 1:
        p = 0.5 * PROBS["mutation"] + 0.5 * (1 - PROBS["mutation"])
    elif assumed_condition[person]["num_genes"] == 2:
        p = PROBS["mutation"]

    return p if num == 0 else (1 - p)


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # TODO looks like every one is using assumed_condition
    # DRY rules?
    # why not make it a global?
    for person in probabilities.keys():
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities.keys():
        total_p = sum([probabilities[person]["gene"][i] for i in range(3)])
        factor = 1 / total_p
        for i in range(3):
            probabilities[person]["gene"][i] *= factor
        
        total_p = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        factor = 1 / total_p
        probabilities[person]["trait"][True] *= factor
        probabilities[person]["trait"][False] *= factor


if __name__ == "__main__":
    main()
