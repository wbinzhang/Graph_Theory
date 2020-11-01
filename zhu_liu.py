import numpy as np

# 定义网络的属性
class Edge(object):
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

    def __str__(self):
        return str(self.u) + str(self.v) + str(self.w)

'''获取网络各条边的信息'''
def get_edges():
    n, m, root = list(map(int, input('请输入网络的顶点个数、其边数以及网络的根（以空格分隔,例如：5 6 1）：\n').split()))

    # 输入各条边的信息
    edges = []
    for i in range(m):
        u, v, w = list(map(int, input(f'请输入网络第{i + 1}/{m}条边的信息（以空格分隔，例如：1 2 5）：\n').split()))
        # 输入的点是1开始的，-1改为0开始的
        edges.append(Edge(u - 1, v - 1, w))

    return n, m, root, edges


'''定义三个关键图：D、H、C(圈)
Step 1
'''
def in_edge(edges, n, m):
    # 顶点个数
    #     V = n
    INF = 999
    while True:
        H_pre = [-1] * n
        H_in_weight = [INF] * n
        # 寻找最小入边
        #         in_weight[root] = 0
        for i in range(m):
            if edges[i].u != edges[i].v and edges[i].w < H_in_weight[edges[i].v]:
                H_pre[edges[i].v] = edges[i].u
                H_in_weight[edges[i].v] = edges[i].w

            #         if H_pre[root] == -1:
        #             F = len(H_pre) - 1
        #         else:
        #             F = len(H_pre)

        F = np.sum(list(map(lambda x: x > -1, H_pre)))
        return H_pre, H_in_weight, F

        # 有孤立点，不存在最小树形图
        for i in range(n):
            if i != root and H_in_weight[i] == INF:
                return '不存在最小树形图'


'''
Step 2
在H中找圈
F为弧集，V为顶点数
'''

INF = 999

def find_circle(H_pre, H_in_weight, F, V, P):
    if F < V - 1:
        print('网络D中没有支撑树形图')
    elif F == V - 1:
        pass

    else:
        # zhuan
        # 去掉一条权重最大的弧
        # 寻找圈中最大的权
        max_weight = H_in_weight.copy()
        while 999 in max_weight:
            max_weight.remove(999)

        index_id = H_in_weight.index(max(max_weight))
        H_pre[index_id] = -1
        H_in_weight[index_id] = INF
    #     return pre, in_weight

    # 寻找圈
    #     circle_change = [-1] * V
    #     circle_final = [-1] * V
    #     c_in_weight = [INF] * n

    circle_num = 0
    length = len([i for i in H_pre if i > -1])

    for i in range(P):
        # 动态圈
        circle_change = [-1] * P
        # 最终的圈
        circle_final = [-1] * P
        # 最终圈的权重
        C_in_weight = [INF] * P
        step = 0
        v = i
        while H_pre[v] != -1 and step <= length:
            circle_change[v] = H_pre[v]

            if circle_change[circle_change[v]] != -1:
                #                 print('出现圈')
                c_v = v
                while circle_change[c_v] not in circle_final:
                    circle_final[c_v] = circle_change[c_v]
                    C_in_weight[c_v] = H_in_weight[c_v]
                    c_v = circle_change[c_v]
                circle_num += 1

            v = H_pre[v]
            step += 1

        if circle_num == 1:
            break

    if circle_num == 0:
        # 最小生成树产生
        # 转step4、5
        return H_pre, H_in_weight, 0

    else:
        return circle_final, C_in_weight, 1
#     return circle_final, C_in_weight

'''
Step 3
塌缩环，对D进行收缩
'''

def systole(D_edges, circle_final, C_in_weight, P):
    #     change_D_edges = []

    #     寻找圈中最大的权
    max_weight = C_in_weight.copy()
    while 999 in max_weight:
        max_weight.remove(999)

    for i in range(len(D_edges)):
        if D_edges[i].v in circle_final:
            if D_edges[i].u not in circle_final:
                for j in circle_final:
                    if D_edges[i].v == j:
                        #                         print(D_edges[i].w, C_in_weight[circle_final.index(j)], max(max_weight))
                        D_edges.append(Edge(D_edges[i].u, P, (int(D_edges[i].w) - C_in_weight[j] + max(max_weight))))
                        D_edges[i].w = INF

            else:
                D_edges[i].w = INF

        if D_edges[i].u in circle_final:
            D_edges[i].u = P

    return D_edges

def zhu_liu(edges, n, m, root):
    circle_dir = {}
    circle_weight_dir = {}

    # H_dir = {}
    # H_weight = {}

    D_edges_dir = {}
    V = n
    P = n

    E = []
    for i in range(len(edges)):
        E.append([edges[i].u, edges[i].v, edges[i].w])
    D_edges_dir[1] = E

    for i in range(100):

        H_pre, H_in_weight, F = in_edge(edges, n, m)

        # H_dir[i + 1] = H_pre
        # H_weight[i + 1] = H_in_weight

        #     V = 6
        #     P = 6
        circle_final, C_in_weight, Q = find_circle(H_pre, H_in_weight, F, V, P)

        circle_dir[i + 1] = circle_final
        circle_weight_dir[i + 1] = C_in_weight

        point_num = len([i for i in circle_final if i > -1])

        if Q == 0:
            break

        D_edges = systole(edges, circle_final, C_in_weight, P)
        #     print(D_edges)
        E = []
        for j in range(len(D_edges)):
            E.append([D_edges[j].u, D_edges[j].v, D_edges[j].w])

        D_edges_dir[i + 2] = E
        #         print(D_edges[j].u, D_edges[j].v, D_edges[j].w)

        #     D_edges_dir[i+1] = D_edges

        V = V - point_num + 1
        P = P + 1
        n = P
        m = len(D_edges)
        edges = D_edges

    return D_edges_dir, circle_dir, circle_weight_dir, circle_final, C_in_weight


def reduction(D_edges_dir, circle_dir, circle_final, circle_weight_dir):
    # print(circle_dir, circle_weight_dir, circle_final, C_in_weight)
    Step = len(D_edges_dir)
    Y = len(circle_final) - 1

    # H_tree = []
    # for i in range(len(circle_final)):
    #     H_tree.append(Edge(circle_final[i], i, C_in_weight[i]))

    while Step > 1:

        C_edge = circle_dir[Step - 1]
        C_weight = circle_weight_dir[Step - 1]
        C_max_weight = C_weight.copy()
        while 999 in C_max_weight:
            C_max_weight.remove(999)

        index_id = C_weight.index(max(C_max_weight))
        C_edge[index_id] = -1
        # H_in_weight[index_id] = INF

        for i in range(len(C_edge)):
            if C_edge[i] != -1:
                circle_final[i] = C_edge[i]
                C_in_weight[i] = C_weight[i]

        for i in range(len(D_edges_dir[Step - 1])):
            if D_edges_dir[Step - 1][i][0] == circle_final[Y] and D_edges_dir[Step - 1][i][2] != 999:
                circle_final[D_edges_dir[Step - 1][i][1]] = circle_final[Y]
                circle_final[Y] = -1

        for i in range(len(circle_final)):
            if circle_final[i] == Y:
                for j in range(len(D_edges_dir[Step - 1])):
                    if D_edges_dir[Step - 1][j][1] == i and circle_final[D_edges_dir[Step - 1][j][0]] != -1:
                        circle_final[i] = D_edges_dir[Step - 1][j][0]

        Step = Step - 1
        Y = Y - 1

    # print(circle_final)
    return  circle_final


if __name__ == "__main__":
    n, m, root, edges = get_edges()
    D_edges_dir, circle_dir, circle_weight_dir, circle_final, C_in_weight = zhu_liu(edges, n, m, root)
    min_tree = reduction(D_edges_dir, circle_dir, circle_final, circle_weight_dir)


    print(min_tree)
    print('朱—刘算法求得的最小树形图为：')
    for i in range(len(min_tree)):
        if min_tree[i] != -1:
            print(f'v_{min_tree[i]+1}—>v_{i+1}')
        else:
            continue













