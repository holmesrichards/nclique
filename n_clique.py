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

def cwords (cliq, words):
        return [words[i][0] for i in cliq]

def clq_find(clq, Ni, words):
        # clq = clique so far
        # Ni = list of indices to check
        # words = graph of words
        
        # Returns true if clique(s) found

        global mxf, Cliques

        foundclq = False
        for j in Ni:
                if j <= clq[-1]:
                        continue
                foundclq = True
                
                # the remaining candidates are only the words in the intersection
                # of the neighborhood sets of i and j
                Nij = Ni & words[j][1]
                foundx = False
                if len(Nij) >= mxf-len(clq)-1:
                        foundx = clq_find (clq+[j], Nij, words)
                if foundx == 0:
                        clqj = clq+[j]
                        if len(clqj) == mxf:
                                Cliques.append(clqj)
                                print (cwords (clqj, words))
                        elif len(clqj) > mxf:
                                Cliques = [clqj]
                                mxf = len(clqj)
                                print ('mxf = ', mxf, ':', cwords (clqj, words))

        return foundclq

def main():

        if len(argv) < 2:
                nchar = '5'
        else:
                nchar = argv[1]

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
        with open('cliques_'+nchar+'.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter = '\t')
                for cliq in Cliques:
                        # get word representation of cliques and write to output
                        cliq_words = cwords (cliq, words)
                        writer.writerow(cliq_words)

main()
