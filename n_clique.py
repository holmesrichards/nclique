"""
# Copyright (C) 2022 - Benjamin Paassen

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import csv
from tqdm import tqdm
from sys import argv

mxf = 0 # mxf = max clique length found so far
Cliques = []
nctotmin = 0 # minimum total letters

def cwords (cliq, words):
        return [words[i][0] for i in cliq]

def clq_find(clq, Ni, words):
        # clq = clique so far
        # Ni = list of indices to check
        # words = graph of words

        # Given a clique, see if it can be extended. If not, and if it
        # is long enough, store it. If it can, call recursively to
        # try to extend it more.
        
        # Returns true if clique(s) found

        global mxf, Cliques

        foundclq = False
        for j in Ni: # check each candidate
                if j <= clq[-1]:
                        continue
                foundclq = True  # clique can be extended by j

                # See if it can be extended further
                # New list of candidates, only the words in the intersection
                # of the neighborhood sets of i and j
                Nij = Ni & words[j][1]
                clqj = clq+[j]
                if len(Nij) < mxf-len(clqj) or \
                   not clq_find (clqj, Nij, words):
                        # Can't extend further, so add clqj to list
                        if nctotmin > 0: # reject if too short
                                if sum([len(words[i][0]) for i in clqj]) < nctotmin:
                                        continue
                        if len(clqj) == mxf:
                                Cliques.append(clqj)
                                # print (cwords (clqj, words))
                        elif len(clqj) > mxf:
                                Cliques = [clqj]
                                mxf = len(clqj)
                                print ('mxf = ', mxf, ':', cwords (clqj, words))

        return foundclq

def main():

        global nctotmin
        
        if len(argv) < 2:
                nchar = '5'
        else:
                nchar = argv[1]
        if len(argv) < 3:
                nctotmin = 0
        else:
                nctotmin = int(argv[2])

        # Here, now, begins the daunting task of finding maximal cliques in the graph we
        # prepared via 'generate_graph.py'.

        print('--- loading graph ---')

        # load the graph first
        words = []
        with open('word_graph_'+nchar+'.csv', newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter = '\t')
                for row in tqdm(reader):
                        word = row[0]
                        neighbor_string = row[1]
                        if neighbor_string == '[]':
                                neighbors = set([])
                        else:
                                neighbors = set([int(neighbor) for neighbor in neighbor_string[1:-1].split(', ')])
                        words.append((row[0], neighbors))

        print('--- start clique finding (THIS WILL TAKE LONG!) ---')

        # start clique finding
        for i in tqdm(range(len(words))):
                Ni = words[i][1]
                clq_find([i], Ni, words)

        print('completed! Found %d cliques' % len(Cliques))

        print('--- write to output ---')
        ofname = 'cliques_'+nchar+'.csv' if nctotmin == 0 else 'cliques_'+nchar+'_'+str(nctotmin)+'.csv'
        with open(ofname, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter = '\t')
                for cliq in Cliques:
                        # get word representation of cliques and write to output
                        cliq_words = cwords (cliq, words)
                        writer.writerow(cliq_words)

main()
