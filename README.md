# n Clique

A generalization of Benjamin Paassen's solution to the problem of finding five English words with 25 distinct characters, using graph theory. This version finds all maximal-length sets of English words of n letters with distinct characters.

Paassen's version is copyright (C) 2022 - Benjamin Paassen
and may be found at [https://gitlab.com/bpaassen/five_clique](https://gitlab.com/bpaassen/five_clique).

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

Following description and quickstart are slightly amended from Paassen's README.  For more on my version and results see this [blog post](https://mathematrec.wordpress.com/2022/08/03/can-you-find-m-n-letter-words-with-nxm-unique-letters/).


## Description

This solution is inspired by the wonderful [A problem squared podcast](https://aproblemsquared.libsyn.com/) by Hill and Parker. In episode 38, Hill and Parker are searching for five English words with distinct letters. Parker's proposed solution builds pairs of distinct words and then tries to merge these pairs to groups of five (henceforth named 'The Parker algorithm'). According to Parker, executing Parker's algorithm on a laptop took about a month. This appeared to the author as optimizable.

The solution proposed here represents the problem as a graph. In particular, we consider all n-letter words (without repeated letters) of the English language as nodes in a graph, and we say that two words are neighbors if they share no letters. Finding m<=floor(26/n) words with distinct letters now is equivalent to finding an [m-clique](https://en.wikipedia.org/wiki/Clique_(graph_theory)) in this graph, meaning a cluster of m words where each word is neighbor to each other word in the cluster.

How do we find an m-clique, then? To find a 5-clique, for example, we start at some word i and build a clique from there. First, we consider all neighbors j. The third word k in the clique now needs to be neighbor to both i and j. Therefore, we consider only words k in the intersection of the neighbor sets of i and j. Next, we consider words l in the intersection of the neighbor sets of i, j, and k. Finally, any words r in the intersection of the neighbor sets of i, j, k, and l form a 5-clique {i, j, k, l, r}. To avoid repitions, we only consider solutions where i < j < k < l < r.

To generalize this, we convert Paassen's nested loops into a recursive function and start looking for cliques. We store the length of the longest clique found and then store only cliques equal to that length; if a longer clique is found, we start the list over again with the longer clique. The result is we find all cliques of maximum length.

In the worst case, this scheme has a complexity of O(k^m), where k is the number of n-letter words in the English language. This may seem infeasible. However, the size of the intersection rapidly declines the deeper we go into the clique. Therefore, we (Paassen) are finished (in the n=5 case) in 21 minutes and 46 seconds, rather than a month, as in the Parker algorithm.

But Parker gave it a go. And that's something.

## Quickstart guide

To reproduce my calculation, please execute the following steps:

1. Download the `words_alpha.txt` file from https://github.com/dwyl/english-words (this is the same file that Parker used).
2. Run the `generate_graph.py` file, adding the path of the words file (defaulting to words_alpha.txt in the current directory) and n (defaulting to 5) as arguments. (should take at most a few minutes for most cases). Add a + sign after n to use words of n *or more* letters.
3. Run the `n_clique.py` file, adding n or n+ as an argument (defaulting to 5). Optionally add an argument for the minimum total number of characters in the clique. (should take at most a few hours for most cases)

All m-word groups with distinct letters should then be in the file `cliques_<args>.csv` where `<args>` reflects the arguments given to `n_clicque.py`.

Examples:

* To find cliques of 5-letter words:
    * `python3 generate_graph.py ~path/to/words_alpha.txt 5` 
    * `python3 n_clique.py 5`
    * Results are in `cliques_5.csv`
* To find cliques of words with 9 or more letters having a total of 20 or more letters:
    * `generate_graph.py ~path/to/words_alpha.txt 9+`
    * `python3 n_clique.py 9+ 20`
    * Results are in `cliques_9+_20.csv`

## Some results

| Length of words | Minimal number of characters | Maximal clique size| Number of cliques found | Note |
|-----|----|--|----|------|
| 4   |-| 6 | bazillions  | long run time and not very interesting|
| 5   |-| 5 | 831  | |
| 6   |-| 4 | 5  |   |
| 7   |-| 3 | 1877 | |
| 8   |-| 2 | 53,013 | no 3-cliques found    |
| 9   |-| 2 | 798  | |
| 10|-| 2 | 1    |  'blacksmith gunpowdery'  |
| 11|-| 2 | 0    |   |
| 12|-| 2 | 0    |   |
| 9 | 20 | 2 | 2 | 'blacksmith gunpowdery' and  'showjumping veldcraft'|
