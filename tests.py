import os
import random
import re
import sys
import pagerank

if len(sys.argv) != 2:
    sys.exit("Usage: python pagerank.py corpus")
corpus = pagerank.crawl(sys.argv[1])

# Test sampling
# print(pagerank.sample_pagerank(corpus, 0.8, 100))

# Test iteration
print(pagerank.iterate_pagerank(corpus, 0.8))