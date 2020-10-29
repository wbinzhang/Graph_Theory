import numpy as np

class Solve_Ford(object):
    def __init__(self,graph_list):
        self.weight = [999] * len(graph_list)
        self.path = [1]*len(graph_list)

    # Ford算法实现
    def Ford(self, k, graph_list):
        # 判断图是否为空，如果为空直接退出
        if graph_list is None:
            return None

        # 格式化矩阵
        graph_matrix = np.array(graph_list)
        if k ==0:
            for i in range(len(graph_list)):
                self.weight[i] = graph_matrix[0, i]

        else:
            dup_weight = self.weight.copy()
            for j in range(len(graph_matrix)):
                for w in range(len(self.weight)):
                    if graph_matrix[w, j] != 999 and (self.weight[w] + graph_matrix[w, j]) < dup_weight[j]:
                        dup_weight[j] = self.weight[w] + graph_matrix[w, j]
                        self.path[j] = str(self.path[w]) + '-' + str(w + 1)
                    else:
                        continue
            self.weight = dup_weight

        return k+1

if __name__=='__main__':
    graph_list = [[0, 1, 5, 999, 3],
                  [999, 0, 2, 999, 999],
                  [999, 999, 0, 999, -4],
                  [999, 999, 2, 0, 999],
                  [999, 999, 999, 3, 0]]

    solve_ford = Solve_Ford(graph_list)
    k = 0
    while k < len(graph_list):
        k = solve_ford.Ford(k, graph_list)

    print('Ford算法求得的从顶点v_1到其余各点的最短路路径、权重分别为：')
    for i in range(1,len(graph_list)+1):
        print('P_%d：%s-%d ； w(P_%d) = %d'%(i, solve_ford.path[i-1],i, i, solve_ford.weight[i-1]))
