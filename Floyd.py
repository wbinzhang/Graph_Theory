import numpy as np

class Edge(object):
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

    def __str__(self):
        return str(self.u) + str(self.v) + str(self.w)


'''获取网络各条边的信息'''
def get_edges():
    n, m = list(map(int, input('请输入网络的顶点个数及其边数（以空格分隔,例如：5 6）：\n').split()))

    # 输入各条边的信息
    edges = []
    for i in range(m):
        u, v, w = list(map(int, input(f'请输入网络第{i + 1}/{m}条边的信息（以空格分隔，例如：1 2 5）：\n').split()))
        # 输入的点是1开始的，-1改为0开始的
        edges.append(Edge(u - 1, v - 1, w))

    return n, m, edges



class Solve_Floyd(object):
    def __init__(self, n):
        self.U_matrix = np.zeros((n, n), dtype=np.int32)
        self.R_matrix = np.zeros((n, n), dtype=np.int32)

    '''将网络转换成矩阵表达'''
    def get_graph(self, n, edges):
        graph_matrix = np.full(shape=(n, n),fill_value=999)
        for edge in edges:
            graph_matrix[edge.u, edge.v] = edge.w
        for i in range(n):
            graph_matrix[i, i] = 0

        return graph_matrix

    # Floyd算法实现
    def Floyd(self, k, graph_matrix):
        if k == 0:
            for i in range(len(graph_matrix)):
                for j in range(len(graph_matrix)):
                    self.U_matrix[i, j] = graph_matrix[i, j]
                    self.R_matrix[i, j] = j
        else:
            for m in range(len(self.U_matrix)):
                for n in range(len(self.R_matrix)):
                    if self.U_matrix[m, n] > self.U_matrix[m, k-1] + self.U_matrix[k-1, n]:
                        self.U_matrix[m, n] = self.U_matrix[m, k-1] + self.U_matrix[k-1, n]
                        self.R_matrix[m, n] = self.R_matrix[m, k-1]
        # print(self.U_matrix, self.R_matrix)

        return self.U_matrix, self.R_matrix, k + 1

if __name__=='__main__':
    # graph_list = [[0, 4, 5, 999, 999],
    #               [999, 0, 3, 999, 6],
    #               [999, 999, 0, -2, 3],
    #               [999, 1, 999, 0, 999],
    #               [-4, 999, 999, 2, 0]]

    n, m, edges = get_edges()
    solve_floyd = Solve_Floyd(n)
    graph_matrix = solve_floyd.get_graph(n, edges)
    k = 0
    while k <= len(graph_matrix):
        U_matrix, R_matrix, k = solve_floyd.Floyd(k, graph_matrix)

    # print('Floyd算法求得的所有顶点之间的最短路和对应的权重如下：')
    print(U_matrix)
    print(R_matrix)
    # final_R_matrix = np.mat(R_matrix.copy()).astype('<U2')
    # print(final_R_matrix)