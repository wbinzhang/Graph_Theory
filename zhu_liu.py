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
        edges.append(Edge(u - 1, v - 1, w))             # 输入的点是1开始的，-1改为0开始的

    for edge in edges:
        if edge.v == root - 1:
            edge.w = 999

    return n, m, root, edges


'''定义朱-刘算法的三个关键图：D图、H图、C(圈)
Step 1
'''
def in_edge(edges, n):
    while True:
        H_pre = [-1] * n                # H_pre用来表示最小入弧集，用列表存储
        H_in_weight = [999] * n             # H_in_weight表示最小入弧的权重，用列表存储，初始为无穷

        '''寻找最小入边'''

        for edge in edges:
            if edge.u != edge.v and edge.w < H_in_weight[edge.v]:
                H_pre[edge.v] = edge.u
                H_in_weight[edge.v] = edge.w

        F = np.sum(list(map(lambda x: x > -1, H_pre)))              # 计算最小入弧弧集的个数

        return H_pre, H_in_weight, F

'''
Step 2
在H中找圈
F为弧集，V为顶点数
'''

def find_circle(H_pre, H_in_weight, F, V, P):               # F表示最小弧集的个数，V表示实际图顶点的个数，P表示所有顶点
    if F < V - 1:
        print('网络D中没有支撑树形图')

    elif F == V - 1:
        pass

    else:

        '''去掉一条权重最大的弧，寻找圈中最大的权'''
        max_weight = H_in_weight.copy()             # 创建权重的副本
        while 999 in max_weight:
            max_weight.remove(999)

        index_id = H_in_weight.index(max(max_weight))               # 返回最大权重所在边的头
        H_pre[index_id] = -1                # 去掉权重
        H_in_weight[index_id] = 999             # 设置权重为999
    #     return pre, in_weight

    '''寻找圈'''
    circle_num = 0              # 初始化圈的数量为0
    length = len([i for i in H_pre if i > -1])              # 计算H_pre孤立点外的点

    '''遍历所有的点寻找圈'''
    for i in range(P):
        circle_change = [-1] * P                # 动态圈
        circle_final = [-1] * P             # 最终的圈
        C_in_weight = [999] * P             # 最终圈的权重
        step = 0                # 初始化计算步骤，步骤达到非孤立点的总和时停止，圈的长度不可能超过非孤立点的总和
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
                break

            v = H_pre[v]
            step += 1

        if circle_num == 1:
            break

    if circle_num == 0:
        '''最小生成树产生，转step4、5，0、1表示状态信息'''
        return H_pre, H_in_weight, 0                # 如果没有圈，返回H_pre

    else:
        return circle_final, C_in_weight, 1
#     return circle_final, C_in_weight

'''
Step 3
塌缩环，对图D进行收缩
'''

def systole(D_edges, circle_final, C_in_weight, P):
    # 寻找圈中最大的权
    max_weight = C_in_weight.copy()
    while 999 in max_weight:
        max_weight.remove(999)

    for D_edge in D_edges:
        if D_edge.v in circle_final:
            if D_edge.u not in circle_final:
                for j in circle_final:
                    if D_edge.v == j:
                        # print(D_edges[i].w, C_in_weight[circle_final.index(j)], max(max_weight))
                        D_edges.append(Edge(D_edge.u, P, (int(D_edge.w) - C_in_weight[j] + max(max_weight))))
                        D_edge.w = 999

            else:
                D_edge.w = 999

        if D_edge.u in circle_final:
            D_edge.u = P

    return D_edges

'''运行实现朱刘算法'''
def zhu_liu(edges, n):
    '''用字典来存储计算过程中产生的圈 C、和图 D'''
    circle_dir = {}             # 初始化存储圈的字典
    circle_weight_dir = {}              # 初始化圈的权重

    D_edges_dir = {}                # 初始化存储图D的字典
    V = n               # 初始化有效顶点V
    P = n               # 初始化所有顶点P

    E = []
    for edge in edges:
        E.append([edge.u, edge.v, edge.w])

    D_edges_dir[1] = E              # 放入第一个图D

    '''执行朱-刘算法，设置循环100次，符合条件自动跳出中断循环'''
    for i in range(100):
        H_pre, H_in_weight, F = in_edge(edges, n)               # 寻找最小入弧

        '''寻找圈 C'''
        circle_final, C_in_weight, Q = find_circle(H_pre, H_in_weight, F, V, P)

        '''将圈的信息存入字典'''
        circle_dir[i + 1] = circle_final
        circle_weight_dir[i + 1] = C_in_weight

        point_num = len([i for i in circle_final if i > -1])                # 计算圈的点数

        '''依据状态值，判断是否跳出循环'''
        if Q == 0:
            break

        '''有环继续进行循环'''
        D_edges = systole(edges, circle_final, C_in_weight, P)              # 对环进行塌缩

        '''将塌缩环后形成的图D存入字典'''
        E = []
        for D_edge in D_edges:
            E.append([D_edge.u, D_edge.v, D_edge.w])

        '''存入字典'''
        D_edges_dir[i + 2] = E

        '''更新变量'''
        V = V - point_num + 1               # 计算图D塌缩后的顶点数
        P = P + 1               # 所有顶点数
        n = P
        # m = len(D_edges)
        edges = D_edges

    return D_edges_dir, circle_dir, circle_weight_dir, circle_final, C_in_weight

'''还原塌缩的图'''
def reduction(D_edges_dir, circle_dir, circle_final, circle_weight_dir):
    # print(circle_dir, circle_weight_dir, circle_final, C_in_weight)
    Step = len(D_edges_dir)             # 还原步骤
    Y = len(circle_final) - 1               # 初始化塌缩点，从后往前还原

    while Step > 1:

        C_edge = circle_dir[Step - 1]
        Base_C_edge = C_edge.copy()
        C_weight = circle_weight_dir[Step - 1]
        if circle_final[Y] != -1:
            for i in range(len(D_edges_dir[Step - 1])):
                if D_edges_dir[Step - 1][i][0] == circle_final[Y] and D_edges_dir[Step - 1][i][1] in circle_dir[Step - 1] and D_edges_dir[Step - 1][i][2] != 999:
                    C_edge[D_edges_dir[Step - 1][i][1]] = -1

        else:
            C_max_weight = C_weight.copy()
            while 999 in C_max_weight:
                C_max_weight.remove(999)
            index_id = C_weight.index(max(C_max_weight))
            C_edge[index_id] = -1

        for i in range(len(C_edge)):
            if C_edge[i] != -1:
                circle_final[i] = C_edge[i]
                # C_in_weight[i] = C_weight[i]

        for i in range(len(D_edges_dir[Step - 1])):
            if D_edges_dir[Step - 1][i][0] == circle_final[Y] and D_edges_dir[Step - 1][i][1] in circle_final and D_edges_dir[Step - 1][i][2] != 999:
                circle_final[D_edges_dir[Step - 1][i][1]] = circle_final[Y]
                circle_final[Y] = -1

        for i in range(len(circle_final)):
            if circle_final[i] == Y:
                for j in range(len(D_edges_dir[Step - 1])):
                    if D_edges_dir[Step - 1][j][1] == i and D_edges_dir[Step - 1][j][0] in Base_C_edge:
                        circle_final[i] = D_edges_dir[Step - 1][j][0]

        Step = Step - 1
        Y = Y - 1

    # print(circle_final)
    return  circle_final, D_edges_dir[1]                # 返回最短路和初始图


if __name__ == "__main__":
    n, m, root, edges = get_edges()
    D_edges_dir, circle_dir, circle_weight_dir, circle_final, C_in_weight = zhu_liu(edges, n)
    min_tree, begin_graph = reduction(D_edges_dir, circle_dir, circle_final, circle_weight_dir)

    # print(min_tree)
    print('朱—刘算法求得的最小树形图为：')
    for i in range(len(min_tree)):
        if min_tree[i] != -1:
            for j in range(len(begin_graph)):
                if begin_graph[j][0] == min_tree[i] and begin_graph[j][1] == i:
                    print(f'v_{int(min_tree[i])+1}—>v_{i+1}，权重为：{begin_graph[j][2]}')
        else:
            continue













