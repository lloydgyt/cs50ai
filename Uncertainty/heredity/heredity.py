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
    # use have_trait, one_gene, two_genes to set all 
    # the Random Variables in Bayesian's Network
    for have_trait in powerset(names):

        # the first half is for fixing EVIDENCE
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
                # only HAVE_TRAIT (evidence) is fixed, loop over all other hidden variable
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
    # a list containing probabilities for everyone with condition setup in question
    proba = list()
    # for each person in people, calculate
    assumed_condition = setup_condition(people, one_gene, two_genes, have_trait)
    for person in people:
        proba.append(proba_person(person, assumed_condition))

    # multiply every proba together
    return math.prod(proba)


def proba_person(person, assumed_condition):
    """
    return the probability PERSON has based in the interested settings
    """
    # collect information needed from ASSUMED_CONDITION
    has_parent = assumed_condition[person]["has_parent"]
    num_genes = assumed_condition[person]["num_genes"]
    trait = assumed_condition[person]["trait"]
    father = assumed_condition[person]["father"]
    mother = assumed_condition[person]["mother"]
    if not has_parent:
        # unconditional proba
        probability = PROBS["gene"][num_genes] * PROBS["trait"][num_genes][trait]
    else:
        # conditional probability based on parents
        # calculate father contribute 0 or 1 genes
        f_0 = pass_num_genes_proba(father, 0, assumed_condition)
        f_1 = pass_num_genes_proba(father, 1, assumed_condition)
        # calculate mother contribute 0 or 1 genes
        m_0 = pass_num_genes_proba(mother, 0, assumed_condition)
        m_1 = pass_num_genes_proba(mother, 1, assumed_condition)

        if num_genes == 0:
            probability_genes = f_0 * m_0
        elif num_genes == 1:
            # either mother contributed 1 and father contributed 0
            # or mother contributed 0 and father contributed 1
            probability_genes = f_0 * m_1 + f_1 * m_0
        elif num_genes == 2: 
            probability_genes = f_1 * m_1

        # compute probability of trait
        probability = probability_genes * PROBS["trait"][num_genes][trait]
    return probability
        

def setup_condition(people, one_gene, two_genes, have_trait):
    """
    Set up condition for everyone (set the value for each random variables in Bayes' network)
    Return a dictionary containing all assumed conditions for everyone.

    Parameters:
    people (dict): A dictionary where keys are people's names and values are dictionaries 
                   containing information about each person, including their mother and father.
    one_gene (set): A set of people who have one gene.
    two_genes (set): A set of people who have two genes.
    have_trait (set): A set of people who have the trait.

    Returns:
    dict: A dictionary where keys are people's names and values are dictionaries containing 
          the following keys:
          - "num_genes": The number of genes the person has (0, 1, or 2).
          - "trait": A boolean indicating whether the person has the trait.
          - "has_parent": A boolean indicating whether the person has a known parent.
          - "mother": The name of the person's mother.
          - "father": The name of the person's father.
    """
    assumed_condition = dict()
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
        has_parent = True if people[person]["mother"] is not None else False
        assumed_condition[person] = {
            "num_genes": num_genes,
            "trait": trait,
            "has_parent": has_parent,
            "mother": people[person]["mother"],
            "father": people[person]["father"]
        }
    return assumed_condition


def pass_num_genes_proba(person, num, assumed_condition):
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
    for person in probabilities.keys():
        # everyone will be added p twice, once in ["gene"], once in ["trait"]
        # because we'll print these 2 probabilities for each person finally
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
