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

class Solve_Ford(object):
    def __init__(self, n):
        self.weight = [999] * n
        self.path = [1] * n

    '''将网络转换成矩阵表达'''
    def get_graph(self, n, edges):
        graph_matrix = np.full(shape=(n, n),fill_value=999)
        for edge in edges:
            graph_matrix[edge.u, edge.v] = edge.w
        for i in range(n):
            graph_matrix[i, i] = 0

        return graph_matrix

    # Ford算法实现
    def Ford(self, k, graph_matrix):

        if k ==0:
            for i in range(n):
                self.weight[i] = graph_matrix[0, i]

        else:
            dup_weight = self.weight.copy()
            for j in range(len(graph_matrix)):
                for w in range(len(self.weight)):
                    if graph_matrix[w, j] != 999 and (self.weight[w] + graph_matrix[w, j]) < dup_weight[j]:
                        dup_weight[j] = self.weight[w] + graph_matrix[w, j]
                        self.path[j] = str(self.path[w]) + '—>' + str(w + 1)
                    else:
                        continue
            self.weight = dup_weight

        return k+1

if __name__=='__main__':
    # graph_list = [[0, 1, 5, 999, 3],
    #               [999, 0, 2, 999, 999],
    #               [999, 999, 0, 999, -4],
    #               [999, 999, 2, 0, 999],
    #               [999, 999, 999, 3, 0]]

    n, m, edges = get_edges()
    solve_ford = Solve_Ford(n)
    graph_matrix = solve_ford.get_graph(n, edges)
    k = 0
    while k < n:
        k = solve_ford.Ford(k, graph_matrix)

    print('Ford算法求得的从顶点v_1到其余各点的最短路路径、权重分别为：')
    for i in range(1,n + 1):
        print(f'P_{i}：{solve_ford.path[i-1]}—>{i} ； w(P_{i}) = {solve_ford.weight[i-1]}')
