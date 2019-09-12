from . import config
from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

STATE_WAITING = 0
STATE_RUNNING = 1
STATE_SUCCEED = 2
STATE_FAILED = 3
STATE_FINISH = 4

Base = declarative_base()

#schema 定义

#图表
class Graph(Base):
    __tablename__ = "graph"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False, unique=True)
    desc = Column(String(128), nullable=True)

    #经常从图查看所有的顶点,边的信息
    vertexes = relationship('Vertex')
    edges = relationship('Edge')


#顶点表
class Vertex(Base):
    __tablename__ = 'vertex'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    input = Column(String(128))
    script = Column(Text, nullable=True)
    g_id = Column(Integer, ForeignKey('graph.id'), nullable=False)

    graph = relationship('Graph')
    #从顶点查看它的边,这里必须使用foreign_keys, 其值必须使用引号
    tails = relationship('Edge', Foreign_keys='[Edge.tail]')
    heads = relationship('Edge', Foreign_keys='Edge.head')


#边表
class Edge(Base):
    __tablename__ = 'edge'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tail = Column(Integer, ForeignKey('vertex.id'), nullable=False)
    head = Column(Integer, ForeignKey('vertex.id'), nullable=False)
    g_id = Column(Integer, ForeignKey('graph.id'), nullable=False)


#Engine
#pipeline表
class Pipeline(Base):
    __tablename__ = 'pipeline'

    id = Column(Integer, primary_key=True, autoincrement=True)
    g_id = Column(Integer, ForeignKey('graph.id'), nullable=False)
    current = Column(Integer, ForeignKey('vertex.id'), nullable=False)
    state = Column(Integer, nullable=False, default=STATE_WAITING)

    vertex = relationship('Vertex')

#路径表
class Track(Base):
    __tablename__ = 'track'

    id = Column(Integer, primary_key=True, autoincrement=True)
    p_id = Column(Integer, ForeignKey('pipeline.id'), nullable=False)
    v_id = Column(Integer, ForeignKey('vertex.id'), nullable=False)
    state = Column(Integer, nullable=False, default=STATE_WAITING)
    input = Column(Text, nullable=True)
    output = Column(Text)

    vertex = relationship('Vertex')
    pipeline = relationship('Pipeline')

class Database:
    _engine = create_engine(config.URL, echo=config.DATABASE_DEBUG)  #属性的单实例,类加载时候即创建连接
    _Session = sessionmaker(bind=_engine)
    _session = _Session()














