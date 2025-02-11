import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    proba_distribution = {}
    modified_corpus = no_link_to_all_links(corpus)
    num_pages = len(modified_corpus)
    num_link_pages = len(modified_corpus[page])

    for p in modified_corpus:
        proba_distribution[p] = (1 - damping_factor) * (1 / num_pages)

    for link_p in modified_corpus[page]:
        proba_distribution[link_p] += damping_factor * (1 / num_link_pages)
    
    return proba_distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    previous_page = random.choice(list(corpus))
    # initialize pageranks
    pageranks = {}
    for p in corpus:
        pageranks[p] = 0

    for i in range(n):
        # use transition_model to get probability distribution 
        proba_distribution = transition_model(corpus, previous_page, damping_factor)
        # pick 1 next_page using the distribution 
        pages = list(proba_distribution.keys())
        weights = list(proba_distribution.values())
        next_page = random.choices(pages, weights=weights, k=1)[0]
        # add (1 / n) to pageranks[page]
        pageranks[next_page] += 1 / n        
        # update previous page
        previous_page = next_page
    
    return pageranks



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initialize
    pageranks = {}
    num_pages = len(corpus)
    for p in corpus:
        pageranks[p] = 1 / num_pages

    # treat non-link pages as all-link pages
    modified_corpus = no_link_to_all_links(corpus)    

    # a dict where keys are pages, values are difference between last update
    delta = {}

    while True:
        # update each pages in corpus
        for p in modified_corpus:
            # calculate new_pagerank 
            pagerank_from_incoming = incoming_term(modified_corpus, p, pageranks, damping_factor)
            pagerank_from_nonincoming = (1 - damping_factor) / num_pages
            new_pagerank = pagerank_from_incoming + pagerank_from_nonincoming
            delta[p] = abs(new_pagerank - pageranks[p])
            pageranks[p] = new_pagerank

        # keep iterating until delta < 0.001
        if all([d < 0.001 for d in delta.values()]):
            break

    return pageranks


def incoming_term(corpus, page, current_pageranks, damping_factor):
    """ calculate term in pagerank of PAGE contributed by incoming pages"""
    # get all the incoming pages and the number of there links
    incoming_pageranks_and_num_links = []
    for p in corpus:
        if page in corpus[p]:
            pagerank = current_pageranks[p]
            num_links = len(corpus[p])
            incoming_pageranks_and_num_links.append((pagerank, num_links))
    return damping_factor * sum([PR / NL for PR, NL in incoming_pageranks_and_num_links])

def no_link_to_all_links(corpus):
    """ 
    return the modified version of corpus

    A page that has no links at all should be interpreted as
    having one link for every page in the corpus (including itself).
    """
    modified_corpus = {}
    for p in corpus:
        modified_corpus[p] = corpus[p].copy()
        if len(modified_corpus[p]) == 0:
            # add all pages as link
            for i in corpus:
                modified_corpus[p].add(i)
    return modified_corpus
    


if __name__ == "__main__":
    main()
