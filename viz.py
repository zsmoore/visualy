import os 
import graphviz as gv
import pprint
import sys
import random

def trace_path():

    layout = {}

    for root, dirs, files in os.walk(os.getcwd()):
        current_dict = layout
        path = root.split('/')
        if is_nothing(path[-1]):
            path.pop()
        if is_hidden(path[-1]):
            #hidden folder, skip
            continue
        for folder in path:
            if is_nothing(folder):
                continue
            if folder not in current_dict:
                current_dict[folder] = {}

            current_dict = current_dict[folder]

        for di in dirs:
            if not is_hidden(di):
                current_dict[di] = {}
        for fi in files:
            if not is_hidden(fi):
                current_dict[fi] = None
    return layout

def vis(node, layout, graph, visited):

    visited.add(node)
    if not layout[node]:
       return

    sum_non_dir = sum([.2 if layout[node][neighbor] == None else 0 for neighbor in layout[node]]) + 1
    print(sum_non_dir)
    graph.node(node, **{'width': str(sum_non_dir), 'height': str(sum_non_dir), 'fontsize':str(sum_non_dir * 10)})
    for neighbor in layout[node]:
        if neighbor not in visited:
            vis(neighbor, layout[node], graph, visited)
            if layout[node][neighbor] != None:
                graph.edge(node, neighbor)
    
    return

def is_hidden(name):
    return name[0] == '.'
        
def is_nothing(name):
    return name == ''

def main():
    if len(sys.argv) != 2:
        print('arg length not 2')
        exit()

    root = sys.argv[1]
    os.chdir(root)
    path = trace_path()

    g = gv.Digraph()
    visited = set()

    vis(random.choice(list(path)), path, g, visited)
    g.render(root + '.gv', view=True)


if __name__ == '__main__':
    main()
