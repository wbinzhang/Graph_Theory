import numpy as np

class Solve_Floyd(object):
    def __init__(self, graph_list):
        self.U_matrix = np.zeros((len(graph_list), len(graph_list)), dtype=np.int32)
        self.R_matrix = np.zeros((len(graph_list), len(graph_list)), dtype=np.int32)

    # Floyd算法实现
    def Floyd(self, graph_list):
        # 判断图是否为空，如果为空直接退出
        if graph_list is None:
            return None


    def Floyd(self, k, graph_list):
        # 格式化矩阵
        graph_matrix = np.array(graph_list)
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
    graph_list = [[0, 4, 5, 999, 999],
                  [999, 0, 3, 999, 6],
                  [999, 999, 0, -2, 3],
                  [999, 1, 999, 0, 999],
                  [-4, 999, 999, 2, 0]]

    solve_floyd = Solve_Floyd(graph_list)

    k = 0
    while k <= len(graph_list):
        U_matrix, R_matrix, k = solve_floyd.Floyd(k, graph_list)

    # print('Floyd算法求得的所有顶点之间的最短路和对应的权重如下：')
    print(U_matrix)
    print(R_matrix)
    # final_R_matrix = np.mat(R_matrix.copy()).astype('<U2')
    # print(final_R_matrix)