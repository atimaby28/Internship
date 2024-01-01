# coding=utf-8

import pandas as pd
import msdatabase as md
import Queue


class TreeNode:
    def __init__(self):
        self.db_info = pd.DataFrame(md.Database().dept_select(),
                                    columns=['Dept', 'Par_Dept', 'Dept_Name', 'View_Order'])
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def print_tree(self):
        if self.children:
            for child in self.children:
                child.print_tree()

    # 데이터를 Hashmap으로 변환하는 부분
    def df_to_dict(self):
        hsmap = {}

        k = 0
        for i in self.db_info['Dept']:
            hsmap[i.encode('utf-8')] = k
            k += 1

        return hsmap

    # 트리를 구성하기 위해 배열의 위치에 데이터를 넣는 부분
    def build_tree(self):

        hsmap = self.df_to_dict()

        tree = [[] for _ in range(len(hsmap))]

        k = 0
        for i in range(1, len(hsmap)):
            tree[hsmap[self.db_info['ParDept'][i]]].append(hsmap[self.db_info['Dept'][i]])
            k += 1

        print(tree)

        return tree

    # 부서의 레벨(Level)을 찾는 부분
    def append_level(self, tree, v, x):

        # array to store level of each node
        level = [None] * v
        marked = [False] * v

        # create a queue
        que = Queue.Queue()

        # enqueue element x
        que.put(x)

        # initialize level of source
        # node to 0
        level[x] = 0

        # marked it as visited
        marked[x] = True

        # do until queue is empty
        while not que.empty():

            # get the first element of queue
            x = que.get()

            # traverse neighbors of node x
            for i in range(len(tree[x])):

                # b is neighbor of node x
                b = tree[x][i]

                # if b is not marked already
                if not marked[b]:

                    # enqueue b in queue
                    que.put(b)

                    # level of b nis level of x + 1
                    level[b] = level[x] + 1

                    # mark b
                    marked[b] = True

        li = []
        for i in range(v):
            print(i, "-->", level[i])
            li.append(level[i])

        se = pd.Series(li)
        self.db_info['Level'] = se

        return self.db_info
