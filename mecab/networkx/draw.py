# -*- coding:utf-8 -*-
import sys
import os
import csv
import networkx as nx
import matplotlib.pylab as plt
import matplotlib
from matplotlib import rcParams
reload(sys)
sys.setdefaultencoding('utf-8')
print matplotlib.matplotlib_fname()

# read all csv file in the target folder
PATH = "/home/nelley/MLpractice/mecab/final/"
corpus_list = []

for root, dirs, files in os.walk(PATH):
    for file in files:
        if file.endswith(".csv"):
            with open(PATH + file) as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                corpus_list.append(list(reader)) 

#print corpus_list

# add corpus_list elements into nodes



G = nx.Graph()

G.add_path(['白工','高雄','台北','台中',])

#G.add_edge("a","[1, 白工]",weight=3)
#G.add_edge("a","[1, 高雄]",weight=5)
#G.add_edge("白工","台北",weight=7)
#G.add_edge("台北","台中",weight=9)
#G.add_edge("台中","高雄",weight=11)
print G.node

pos = nx.spring_layout(G)
edge_labels = {("白工","台北"):13,("台北","台中"):15, ("台中","高雄"):11}

nx.draw_networkx_nodes(G, pos, node_size=20, node_color="r")
nx.draw_networkx_edges(G, pos, width=2)
nx.draw_networkx_edge_labels(G, pos,edge_labels)
nx.draw_networkx_labels(G, pos ,font_size=16, font_color="r")

plt.xticks([])
plt.yticks([])
plt.show()
