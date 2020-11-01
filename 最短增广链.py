# coding: utf-8
"""
最短增广链
"""

# 定义网络的属性:tail、head、edge。
class Edge(object):
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

    def __str__(self):
        return str(self.u) + str(self.v) + str(self.w)

def get_edges():
    '''输入顶点n、边数m、根r'''
    s, t, n, m = list(map(int, input('请输入容量网络的发点、收点、顶点个数以及边数（以空格分隔,例如：1 3 3 3）：\n').split()))

    # 输入各条边的信息
    edges = []
    for i in range(m):
        u, v, w = list(map(int, input(f'请输入容量网络第{i+1}/{m}条边的信息（以空格分隔，例如：1 2 5）：\n').split()))
        # 输入的点是1开始的，-1改为0开始的
        edges.append(Edge(u - 1, v - 1, w))

    '''初始化可行流'''
    flows = []
    for edge in edges:
        flows.append(Edge(edge.u, edge.v, 0))

    return s, t, n, m, edges, flows

# 构造剩余网络D
# 定义rn_edges为矩阵
def residual_network(edges, rn_edges):
    gen_rn_edges = []
    for edge in edges:
        if edge.w == rn_edges[edge.u, edge.v]:
            gen_rn_edges.append(Edge(edge.v, edge.u, edge.w))
        elif edge.w > rn_edges[edge.u, edge.v] and rn_edges[edge.u, edge.v] == 0:
            gen_rn_edges.append(Edge(edge.u, edge.v, edge.w))
        else:
            gen_rn_edges.append(Edge(edge.u, edge.v, edge.w - int(rn_edges[edge.u, edge.v])))
            gen_rn_edges.append(Edge(edge.v, edge.u, int(rn_edges[edge.u, edge.v])))
            
    return gen_rn_edges

'''利用广探法构造分层剩余网络：hie_res_net'''
'''定义分层标号函数'''
def hierachical(hie_res_net, next_tail, edges, tail, h):    # 分层标号；next_tail表示已检查和即将要检验点的集合；h为标号——上一层的编号

    for edge in edges:     
        if edge.u == tail and hie_res_net[edge.v] == -1:
            hie_res_net[edge.v] = h
            next_tail.add(edge.v)
        else:
            continue            
            
    return hie_res_net, next_tail

'''构建分层剩余网络'''
def hierachical_residual_network(s, t, n, edges):
    hie_res_net = [-1] * n
    next_tail = {s-1}    # 已检查加下一步需要检查的点
    back_tail = set()    # 创建一个集合，去重；back_tail表示已检查
    h = 0
    unexamined = next_tail - back_tail    # unexamined表示未检查的点
    state = True    # 定义一个状态，判断最大流是否找到
    
    while t-1 not in unexamined:
        if unexamined:
            for tail in unexamined:
                back_tail.add(tail)
                hie_res_net, next_tail = hierachical(hie_res_net, next_tail, edges, tail, h)
            h += 1
            unexamined = next_tail - back_tail
        else:
            print(f'不存在{s}到{t}的路，最大流已找到')
            state = False
            break
    
    return hie_res_net, state

'''在分层剩余网络中寻找一条v_s—v_t的路'''

def getP_fromAD(t, edges, hie_res_net):
    path = [-1]*n    # 初始路径
    weight = [999]*n
    final_path = [-1]*n    # 最终路径
    final_weight = [999]*n

    for edge in edges: 
        if hie_res_net[edge.v] - hie_res_net[edge.u] == 1 and path[edge.v] == -1:
            path[edge.v] = edge.u
            weight[edge.v] = edge.w
    
#     final_path[t-1] = path[t-1]
    head = t-1
    # tail = path[head]
    while head != 0:
        final_path[head] = path[head]
        final_weight[head] = weight[head]
        head = path[head]
    
    return final_path, final_weight

'''沿P进行增广，得到新的可行流'''
def get_flow(edges, flows, path, weight):
    for edge in edges:
        if path[edge.v] == edge.u:
            for flow in flows:
                if edge.u == flow.u and edge.v == flow.v and flow.w != 0:
                     flow.w = min(weight) + flow.w
                
                elif edge.u == flow.u and edge.v == flow.v and flow.w == 0:
                    flow.w = min(weight)
                else:
                    continue
        else:
            continue
            
    return flows

'''调整edges(初始图)'''

def revise_Edges(edges, path, weight):
    revise_edges = []
    for edge in edges:
        if edge.u == path[weight.index(min(weight))] and edge.v == weight.index(min(weight)):
            continue
        elif edge.u in path and edge.v == path.index(edge.u):
            revise_edges.append(Edge(edge.u, edge.v, edge.w - min(weight)))
        
        else:
            revise_edges.append(Edge(edge.u, edge.v, edge.w))
            
    return revise_edges


if __name__=='__main__':
    '''执行算法'''
    s, t, n, m, edges, flows = get_edges()

    '''初始化参数'''
    state = True
    Edges = edges.copy()

    while True:
        hie_res_net, state = hierachical_residual_network(s, t, n, Edges)    #分层剩余网络
        if state == True:
            path, weight = getP_fromAD(t, Edges, hie_res_net)    #寻找v_s-v_t路
            flows = get_flow(edges, flows, path, weight)    #计算更新新的可行流
            revise_edges = revise_Edges(Edges, path, weight)    # 调整edges
            Edges = revise_edges
        else:
            break

    for flow in flows:
        print(f'v_{flow.u + 1}——>v_{flow.v + 1},权重为：{flow.w}')





