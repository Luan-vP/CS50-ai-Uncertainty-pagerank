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

    # Development Shiv --
    print(corpus)
    print(len(corpus.keys()))
    for page in corpus.keys():
        print(page)

    print("transition_model(corpus, '1.html', 0.8)")
    print(transition_model(corpus, '1.html', 0.8))

    # End shiv --

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
    number_of_links = len(corpus[page])

    if number_of_links == 0:
        return { 
            next_page: 1.0 / len(corpus.keys())

            for next_page in corpus.keys()
        }

    link_probability = damping_factor / number_of_links
    random_page_probability = ( 1 - damping_factor ) / len(corpus.keys())

    transition_dictionary = { 
        next_page: link_probability + random_page_probability if next_page in corpus[page] else random_page_probability 

        for next_page in corpus.keys()
    }

    return transition_dictionary


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Count page visits
    count_dictionary = { 
        
        page: 0.0

        for page in corpus.keys()
    }

    # Start from random page
    starting_page = random.sample(corpus.keys(),1)[0]
    print(starting_page)

    count_dictionary[starting_page] += 1

    for _ in range(n-1):

        page_transition_model = transition_model(corpus, starting_page, damping_factor)
        print(page_transition_model)
        
        next_page = random.choices(list(page_transition_model.keys()), list(page_transition_model.values()))[0]

        count_dictionary[next_page] += 1

        starting_page = next_page

    print(sum(count_dictionary.values()))

    print(count_dictionary)

    return {
        page: count_dictionary[page] / n

        for page in corpus
    }


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initialise to 0.5
    page_rank_dict = {
        page: 0.5

        for page in corpus
    }

    


if __name__ == "__main__":
    main()
