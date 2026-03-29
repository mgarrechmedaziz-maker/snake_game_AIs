import numpy as np
import math
import random
class Value():

    def __init__(self,data,_children=(),_op=''):
        self.data=data
        self._prev=set(_children)
        self._op=_op
        self.grad=0.0
        self.name=''
        self._backward= lambda : None
    def __add__(self,other):
        other =other if isinstance(other,Value) else Value(other)
        out=Value(self.data + other.data, {self,other},'+')
        def _backward():
            self.grad+=out.grad
            other.grad+=out.grad
        out._backward=_backward
        return out
    def __radd__(self,other):
        return self+other
    def __sub__ (self,other):
        return self + (-1 * other)
    def __rsub__ (self,other):
        return other + (-1 * self)
    def __mul__(self,other):
        other =other if isinstance(other,Value) else Value(other)
        out=Value(self.data*other.data , {self,other},'*')
        def _backward():
            self.grad+=other.data *out.grad
            other.grad+=self.data*out.grad
        out._backward=_backward   
        return out
    def __rmul__(self,other):
        return self*other
    def __repr__(self):
        return "value(data=" + str(self.data)+")"
    def __pow__(self,n):
        out=1
        for i in range(n) :
            out *= self
        return out     
    def tanh(self):
        out = Value(math.tanh(self.data),{self},'tanh')
        def _backward():
            self.grad+= (1 - pow(out.data,2)) * out.grad
        out._backward=_backward  
        return out
    def backward(self):
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited :
                visited.add(v)
                for child in v._prev :
                    build_topo(child)
                topo.append(v)   
        self.grad=1.0
        build_topo(self)         
        for node in reversed(topo):
            node._backward()             

from graphviz import Digraph

def trace(root):
    # Builds a set of all nodes and edges in a graph
    nodes, edges = set(), set()
    def build(v):
        if v not in nodes:
            nodes.add(v)
            for child in v._prev:
                edges.add((child, v))
                build(child)
    build(root)
    return nodes, edges

def draw_dot(root):
    dot = Digraph(format='svg', graph_attr={'rankdir': 'LR'}) # LR = Left to Right
    
    nodes, edges = trace(root)
    for n in nodes:
        uid = str(id(n))
        
        # For any value in the graph, create a rectangular ('record') node for it
        # This shows the numerical value, the gradient, and the label (if it has one)
        # Note: formatting strings %.4f ensures 4 decimal places
        dot.node(name=uid, label = "{ data %.4f | grad %.4f }" % (n.data, n.grad), shape='record')
        
        # If this value was the result of an operation, create an op node for it
        if n._op:
            # Create the small circle node for the operation (e.g. +, *)
            dot.node(name=uid + n._op, label=n._op)
            # Connect the op node to the value node
            dot.edge(uid + n._op, uid)
    
    for n1, n2 in edges:
        # Connect n1 to the op node of n2
        dot.edge(str(id(n1)), str(id(n2)) + n2._op)
    
    return dot


class neuron():
    def __init__(self,nin):
        self.w=[ Value(random.uniform(-1,1)) for _ in range(nin)]
        self.b=Value(random.uniform(-1,1))
    def __call__(self,x):
        act=sum((w*d for w,d in zip(self.w,x)),self.b)
        out=act.tanh()
        return out
    def parameter(self):
        return self.w +[self.b]
    
class layer():
    def __init__(self,nin,nout):
        self.neurons=[neuron(nin) for _ in range(nout)]
    def __call__(self,x):
        out = [ neuron(x) for neuron in self.neurons]
        return out[0] if len(out)==1 else out
    def parameter(self):
        return [p for neuron in self.neurons for p in neuron.parameter()]
class MLP():
    def __init__(self,nin,nouts):
        sz=[nin] + nouts
        self.layers=[layer(sz[i],sz[i+1]) for i in range(len(nouts))]
    def __call__(self,x):
        for layer in self.layers:
            x = layer(x) 
        return x
    def parameter(self):
        return [p for layer in self.layers for p in layer.parameter()]
    
#a=Value(3.0)
#b=Value(2.0)
n=MLP(3,[3,2,1])
xs= ([2.0,-4.0,6.0],
     [1.0,-6.0,2.0],
     [0.0,-8.0,1.0],
     [7.0,-4.0,12.0])
ys= [1.0,-1.0,-1.0,1.0]
for i in range(20):
    ypred=[n(x) for x in xs]
    loss = sum((ygt - yout)**2 for ygt, yout in zip(ys, ypred))
    
    for param in n.parameter():
        param.grad =0.0
    loss.backward()
    
    
    for param in n.parameter():
        param.data += -0.07 * param.grad
    print(i,loss.data)
print(n.layers[0].neurons[0].w[0].grad)
#draw_dot(loss).render('computational_graph', view=True)