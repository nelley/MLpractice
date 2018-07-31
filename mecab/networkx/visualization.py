# -*- coding:utf-8 -*-
import sys
import networkx as nx
from subprocess import Popen, PIPE
import pdb
import matplotlib.pyplot as plt
reload(sys)
sys.setdefaultencoding('utf-8')


EXCEPTIONS = ['EOS', 'BOS']

def construct_node(cell):
    #check EOS list
    tmp_node = ''
    if all(x not in cell[0] for x in EXCEPTIONS):
        attr_str = ",".join(str(value) for idx, value in enumerate(cell) if idx > 0 and idx < 7)
        cost_str = cell[13]
        tmp_node = cell[0].replace('"','') + '\n' + attr_str + '\n' + cost_str
    else:
        if 'BOS' in cell[0]:
            tmp_node = 'BOS'
        else:
            tmp_node = 'EOS'
    return tmp_node


def put_nodes(d_root, output):
    linelist = output.splitlines()
    nodes = []
    node_pos = []
    cnt = 0
    for idx, line in enumerate(linelist):
        cell = line.split(',')
        #nodes.append(construct_node(cell))
        d_root.add_node(construct_node(cell))
        node_pos.append(cnt)
        # for index of pos
        if 'EOS' not in line:
            cnt+=1
        else:
            cnt=0
    node_pos.append(99)
    return nodes, node_pos


def put_edges(d_root, output):
    linelist = output.splitlines()
    edges = {}
    for idx, line in enumerate(linelist):
        if 'EOS' not in line:
            tmp_tuple = (construct_node(linelist[idx].split(',')), construct_node(linelist[idx+1].split(',')))
            #edges.insert(idx, tmp_tuple)
            cell = linelist[idx+1].split(',')
            print ','.join(str(x) for x in cell)
            edges[tmp_tuple] = int(cell[15]) - int(cell[13])
            #print 'dict value=%s' % edges[tmp_tuple]
            d_root.add_edge(construct_node(linelist[idx].split(',')), construct_node(linelist[idx+1].split(',')))

    return edges


def draw_graph(output):
    linelist = output.splitlines()
    nodes = []
    edges = []
    D = nx.DiGraph()
    #sep_list = []
    for idx, line in enumerate(linelist):
        cell = line.split(',')
        nodes.insert(idx, cell[0].replace('"',''))
 
        tmp_tuple = (linelist[idx].split(',')[0].replace('"',''), linelist[idx+1].split(',')[0].replace('"',''))
        edges.insert(idx, tmp_tuple)
        if "EOS" in  linelist[idx+1].split(',')[0].replace('"',''):
            break
    
    # deploy into networkx
    D.add_nodes_from(nodes)
    D.add_edges_from(edges)
    nx.draw_networkx(D, pos=None, arrow=True, with_labels=True)
    plt.show()
        


if __name__ == "__main__":
    pdb.set_trace()
    '''
    %m:表層文字
    %phl:左ID
    %phr:右ID
    %pb:最適解の時＊、それ以外は空白
    %pw:単語生起コスト
    %pc:連結コスト＋単語生起コスト（文頭あら累計）
    %pn:連結コスト＋単語生起コスト（その形態素単独）
    '''
    p = Popen(['mecab', '-F"%m,%H,%phl,%phr,%pb,%pw,%pc,%pn\n"', '-N3', '-B"BOS\n"', '-EEOS,%H,%phl,%phr,%pb,%pw,%pc,%pn\n'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    #p = Popen(['mecab', '-F"%m,%H,%phl,%phr,%pb,%pw,%pc,%pn\n"', '-N5', '-B"BOS\n"'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate("競合他社をマヌーサ、あるいはメタパニする、ヒャダイインのようにギガデインをする")
    #print output

    nodes_pos = []
    D = nx.DiGraph()
    nodes, node_pos = put_nodes(D, output)
    edge_labels = put_edges(D, output)
    ''' 
    for key, ed in edges_dict.iteritems():
        print key
        print '------xxx-'
    '''
    #edges_list = list(edge_labels.keys())
    #D.add_nodes_from(nodes)
    #D.add_edges_from(edges_list)
    pos = nx.spring_layout(D)
    nx.draw_networkx_nodes(D, pos, node_size=60, node_color='b') 
    nx.draw_networkx_edges(D, pos, width=1)
    nx.draw_networkx_edge_labels(D, pos, edge_labels)
    nx.draw_networkx_labels(D, pos ,font_size=12, font_color="r")
    #nx.draw_networkx(D, pos=nx.spring_layout(D) , arrow=True, with_labels=True)
    plt.show()
    
    #p2 = Popen(['mecab', '-a'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    #output2, err2 = p2.communicate("東京都に住む")
    #print output2
    
