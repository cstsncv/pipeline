#定义流程DAG,即Schema定义
#执行某一个DAG的流程


"""查找所有入度为0的顶点,  不适合验证DAG,需多次查询
SELECT vertex.*
FROM vertex
LEFT JOIN edge ON vertex.id = edge.head AND vertex.g_id = 1 AND edge.g_id =1
WHERE edge.head is NULL"""

from .model import db
from .model import Graph, Vertex, Edge
from .model import Pipeline, Track
from functools import wraps

#装饰器实现统一事务管理
def transactionl(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            ret = fn(*args, **kwargs)
            db.session.commit()
            return ret
        except Exception as e:
            db.session.rollback()
            raise e
    return wrapper

#创建DAG  Graph
@transactionl
def create_graph(name, desc=None):
    g = Graph()
    g.name = name
    g.desc = desc

    db.session.add(g)
    return g

#为DAG增加顶点 Vertex
@transactionl
def add_vertex(graph:Graph, name:str, input=None, script=None):
    v = Vertex()
    v.g_id = graph.id
    v.name = name
    v.input = input
    v.script = script

    db.session.add(v)
    return v

#为DAG增加边Edge
@transactionl
def add_edge(graph:Graph, tail:Vertex, head:Vertex):
    e = Edge()
    e.id = graph.id
    e.tail = tail.id
    e.head = head.id

    db.session.add(e)
    return e

#删除顶点, 需先删除顶点关联的所有边
@transactionl
def del_vertex(id):
    query = db.session.query(Vertex).filter(Vertex.id == id)
    v = query.first()
    if v: #找到顶点后,删除关联的边,然后删除顶点
        db.session.query(Edge).filter((Edge.tail == v.id) | (Edge.head == v.id)).delete()
        query.delete()
    return v


###################################
#测试数据








#########################################
#检测是否一个合法的DAG, kaen算法, 依次删除入度为0的边及顶点,最后为空则是DAG
#一次从数据库取出graph下所有顶点和边,在内存中遍历,避免多次操作数据库,
def check_graph(graph: Graph) -> bool:
    query = db.session.query(Vertex).filter(Vertex.g_id == graph.id)
    vertexes = [vertex.id for vertex in query]   #顶点列表
    query = db.session.query(Edge).filter(Edge.g_id == graph.id)
    edges = [(edge.tail, edge.head) for edge in query]  #边表[(tail, head)]

    #顶点vertexes [1,2,3,4]  边edges[(1,2), (1,3), (3,2), (2,4)]
    #遍历顶点
    while True:
        vis = []
        for i, v in enumerate(vertexes):
            for _, h in edges:
                if v == h: #当前顶点有入度,跳出当前循环
                    break
            else: #没有break,说明遍历一遍边,没有找到顶点作为弧头,就是入度为0
                vis.append(i)
                ejs = []  #找到入度为0的顶点后,删除相关的边后删除本身
                for j, (t, _) in enumerate(edges):
                    if t == v:
                        ejs.append(j)
                for j in reversed(ejs): ###删除列表需逆向删除
                    edges.pop(j)
                break
        else:  #遍历一遍剩余顶点后,都没有break,说明没有找到入度为0的顶点
            return False

        for i in vis:
            vertexes.pop(i)
        print(vertexes, edges)
        if len(vertexes) == 0 and len(edges) == 0:
            #检验通过,修改checked字段为1
            try:
                grapha = db.session.query(Graph).filter(Graph.id == graph.id).first()
                if grapha:
                    grapha.checker = 1
                db.session.add(grapha)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                raise e










