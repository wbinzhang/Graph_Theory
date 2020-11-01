import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

class Edge(object):
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

    def __str__(self):
        return str(self.u) + str(self.v) + str(self.w)


'''获取网络各条边的信息'''
def get_edges():
    n, m = list(map(int, input('请输入图的顶点个数及其边数（以空格分隔,例如：5 6）：\n').split()))

    # 输入各条边的信息
    edges = []
    for i in range(m):
        u, v, w = list(map(int, input(f'请输入网络第{i + 1}/{m}条边的信息（以空格分隔，例如：1 2 5）：\n').split()))
        # 输入的点是1开始的，-1改为0开始的
        edges.append(Edge(u - 1, v - 1, w))

    return n, m, edges

class Solve_Dijkstra(object):
    def __init__(self):
        self.raw = [] #缓存矩阵索引
        self.path = [] #最小生成树路径
        self.m = 0
        self.n = 0

    '''将网络转换成矩阵表达'''
    def get_graph(self, n, edges):
        graph_matrix = np.full(shape=(n, n),fill_value=999)
        for edge in edges:
            graph_matrix[edge.u, edge.v] = edge.w
            graph_matrix[edge.v, edge.u] = edge.w

        return graph_matrix


    # dijkstra算法实现
    def dijkstra(self, graph_matrix):

        #构造一个转移矩阵用来存放最小生成树的权重
        transfer_matrix = np.zeros([len(graph_matrix), len(graph_matrix)])
        # print(transfer_matrix)

        self.Draw_graph(graph_matrix)

        # raw = []
        # path = []
        # path_dic = {}
        # m = 0
        # n = 0

        for i in range(len(graph_matrix)):
            # a = np.delete(graph_matrix, m, axis=1)
            # 把第一列所有元素改为X
            graph_matrix[:, self.m] = 998

            # print('graph_matrix', graph_matrix)

            if graph_matrix.min() == 998:
                print('权重矩阵：', transfer_matrix)
                print('权重总和：', transfer_matrix.sum())
                print('最短路径：', self.path)
                self.Draw_graph(transfer_matrix)

            else:
                # print(transfer_matrix)
                self.raw.append(self.n)
                # print(raw)
                # 设置缓存矩阵
                temp = graph_matrix[self.raw]
                # print(temp)
                r, c = np.where(temp == np.min(temp))
                # print(r, c)

                if temp.min() == 999:
                    print('图不存在支撑树')

                else:
                    transfer_matrix[self.n, int(c[0])] = temp.min()
                    self.path.append([self.n, int(c[0])])
                # print(transfer_matrix)

                self.m = c[0]
                self.n = self.m

    def Draw_graph(self, graph_matrix):
        # 构造一个网格图
        Initial_Graph = nx.Graph()
        # 构建图的标签
        for i in range(len(graph_matrix)):
            for j in range(len(graph_matrix)):
                if graph_matrix[i, j] < 998 and graph_matrix[i, j] > 0:
                    Initial_Graph.add_edge(('v' + str(i)), ('v' + str(j)), weight=int(graph_matrix[i, j]))
                    # Graph_labels[(i, j)] = graph_matrix[i, j]
                else:
                    continue

        # for u, v, d in G.edges(data=True):
        #     print(u, v, d['weight'])
        edge_labels = dict([((u, v,), d['weight']) for u, v, d in Initial_Graph.edges(data=True)])
        # pos = nx.spring_layout(Initial_Graph)
        pos = nx.random_layout(Initial_Graph)
        nx.draw_networkx_edge_labels(Initial_Graph, pos, edge_labels=edge_labels, font_size=14)  # 绘制图中边的权重
        nx.draw_networkx(Initial_Graph, pos, node_size=400)
        plt.show()

if __name__ == '__main__':
    # graph_list = [ [999, 50, 30, 40, 25],
    #         [50, 999, 15, 20, 999],
    #         [30, 15, 999, 10, 20],
    #         [40, 20, 10, 999, 10],
    #         [25, 999, 20, 10, 999]]

    n, m, edges = get_edges()
    solve_dijkstra = Solve_Dijkstra()
    graph_matrix = solve_dijkstra.get_graph(n, edges)
    solve_dijkstra.dijkstra(graph_matrix)
