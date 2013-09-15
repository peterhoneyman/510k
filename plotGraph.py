####################
# This program is used to plot the predicate graph
# and get some statistical data.
# @Author: Tingyi Wei SPQR LAB
####################

import sys
from sets import Set
from collections import deque

def dfs(device, Knumber, visitnode, path):
  # Devide the devices according to the ancestor relationship into groups
  if device == Knumber:
    return 1
  elif device in visitnode:
    return visitnode[device]
  else:
    path_num = 0
    if device in adj_list:
      for next_node in adj_list[device]:
        if next_node in path:
          pathtemp = path[:]
          pathtemp.insert(0, next_node)
          ss = device + "graph %s %s" %(groupindex, pathtemp)
          if ss not in printline:
            printline.append(ss)
            print ss
          return -1
        else:
          pathtemp = path[:]
          pathtemp.insert(0, next_node)         
          path_node = dfs(next_node, Knumber, visitnode, pathtemp)
          if path_node == -1:
            return -1
          else:
            path_num += path_node
    visitnode[device] = path_num
    return path_num


PREDfile = open(sys.argv[1])
remain = []
for line in PREDfile:
  append = 1
  oneline = []
  oneline.append(line[0:7])
  pred = line.find('K', 9)
  if pred == -1:
    append = 0
  while not pred == -1:
    oneline.append(line[pred:pred+7])
    pred = line.find('K', pred+8)
  if append == 1:
    remain.append(oneline)
PREDfile.close()
group = Set()
find = Set()

visited = Set()
GROUPfile = open(sys.argv[2], 'w')
STACfile = open(sys.argv[3], 'w')
DEGREEfile = open(sys.argv[4], 'w')
RPATHfile = open(sys.argv[5], 'w')
groupindex = 1
loopline = []
for idx, firstline in enumerate(remain):
  if not idx in visited:
    visited.add(idx)
    find.update(firstline)
    grouplines = []
    grouplines.append(firstline)
    while len(find) != 0:
      device = find.pop()
      group.add(device)
      for idx2, line in enumerate(remain):
        if not idx2 in visited:
          if device in line:
            visited.add(idx2)
            find.update(line)
            grouplines.append(line)
      find.discard(device)
    for device in group:
      GROUPfile.write(device + ' ')
    GROUPfile.write('\n')
    num_edge = 0
    
    if len(group) > 1:
      adj_list = dict()
      degree_in = {}
      degree_out = {}
      for device in group:
        degree_in[device] = 0
        degree_out[device] = 0
      DOTfile = open("dotfile/%s.dot" % (groupindex), 'w')
      DOTfile.write("digraph G {\n")
      for line in grouplines:
        edges = []
        for idx3, Knumber in enumerate(line):
          if idx3 == 0:
            device = Knumber
          else:
            num_edge += 1
            DOTfile.write("  " + device + "->" + Knumber + ';\n')
            degree_out[device] += 1
            degree_in[Knumber] += 1
            edges.append(Knumber)
        adj_list[device] = edges    
            
      DOTfile.write('}')
      DOTfile.close()
      for device in group:
        DEGREEfile.write(device + "  %s  %s\n" %(degree_in[device], degree_out[device]))
    else:
      DEGREEfile.write(group[0] + " degree in: 0 degree out: 0\n")

    STACfile.write("Graph %s Number of lines: %s Number of Nodes: %s Number of Edges: %s\n" %(groupindex, len(grouplines), len(group), num_edge))
    
    if len(group) > 100:
      print "Graph %s Number of lines: %s Number of Nodes: %s Number of Edges: %s\n" %(groupindex, len(grouplines), len(group), num_edge)

    # Use BFS to find number of redundant paths between devices and their predicates
    if len(group) > 1:
      printline = []
      for line in grouplines:
        device = line[0]
        STACfile.write(device + ": ")
        for idx3, Knumber in enumerate(line):
          if idx3 != 0:
            visitnode = dict()
            path_num_main = dfs(device, Knumber, visitnode, [device])
            if path_num_main != -1:
              STACfile.write(Knumber + "(%s) " %(path_num_main))
              if path_num_main > 1:
                RPATHfile.write(device + '->' + Knumber + "  %s\n" %(path_num_main-1))
              if path_num_main > 50:
                print "Graph %s " %(groupindex) + device + " -> " + Knumber + " (%s)" %(path_num_main)
            else:
              STACfile.write(Knumber + "(NA)")
        STACfile.write("\n")

    group.clear()
    groupindex += 1
GROUPfile.close()
STACfile.close()
DEGREEfile.close()
