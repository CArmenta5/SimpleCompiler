from anytree import Node, RenderTree
from Tokens import Tokens



global index
global lines
index = 0

def peek():
    global index
    global lines
    return lines[index]

def advance():
    global index
    val = peek()
    index = index + 1
    return val

def eof():
    global lines
    global index
    return index >= len(lines)

def scan_digits():
    ans = {
        'val': ''
    }
    while peek() in '0123456789':
        ans['val'] = ans['val'] + advance()
    if peek() != '.':
        ans['type'] = 'inum'
    else:
        ans['type'] = 'fnum'
        ans['val'] = ans['val'] + advance()
        while peek() in '0123456789':
            ans['val'] = ans['val'] + advance()     
    return ans

def scanner():
    ans = {}
    while not eof() and (peek() == ' ' or peek() == '\n'):
        advance()
    if eof():
        ans['type'] = '$'
    else:
        if peek() in '0123456789':
            ans = scan_digits()
        else :
            ch = advance()
            if ch in 'abcdeghjklmnoqrstuvwxyz':
                ans['type'] = 'id'
                ans['val'] = ch
            elif ch == 'f':
                ans['type'] = 'floatdcl'
            elif ch == 'i':
                ans['type'] = 'intdcl'
            elif ch == 'p':
                ans['type'] = 'print'
            elif ch == '=':
                ans['type'] = 'assign'
            elif ch == '+':
                ans['type'] = 'plus'
            elif ch == '-':
                ans['type'] = 'minus'
            else:
                print('error léxico')
                exit()
    return ans


class Nodo:
    def __init__(self, type, data):
        self.type = type
        self.data = data
        self.children = []

    def setType(self, type):
        self.setType = type
    def setVal(self, val):
        self.setVal = val
    def addChildren(self, childs):
        if type(childs) is list:    
            for child in childs:
                self.children.append(child)
        else:
            self.children.append(childs)

#---- Parser code

def expr(tokens):
    token = tokens.peek()
    if token['type'] == 'minus':    
        tokens.next()
        print(token)
        return Nodo(token['type'],'-')
    if token['type'] == 'plus':    
        tokens.next()
        print(token)
        return Nodo(token['type'],'+')
    else:
        return None

def val(tokens):
    token = tokens.peek()
    print(token)
    if token['type'] == 'id' or token['type'] == 'inum'  or token['type'] == 'fnum':    
        tokens.next()
        return Nodo(token['type'],token['val'])
    else:
        print("Error Sintáctico id")
        #exit()

#Utility for matching tokens in an input stream
def match(tokens):
    token = tokens.peek()
    print(token)
    if token['type'] == 'id':
        tokens.next()
        return Nodo(token['type'],token['val'])

    if token['type'] == 'assign':
        tokens.next()
        return Nodo(token['type'], '=')

    if token['type'] == 'print':
        tokens.next()
        tmp = tokens.peek()

        if tmp['type'] == 'id':
            print(tmp)
            tokens.next()
            return Nodo(token['type'], tmp['val'])
        else:
            print("Error Sintáctico Match 1")
            exit()
    else:
        print("Error Sintáctico Match 2")
        #exit()

def stmt(tokens):
    # Nested id assign
    token = tokens.peek()
    if token['type'] == 'id':
        n1_match = match(tokens)#, "id")
        n2_match = match(tokens)#, "assign")
        n2_match.addChildren(n1_match)        

        #Cylce for val(expr val)*
        f_parent = n2_match
        while True:
            n_val = val(tokens)
            t_expr = expr(tokens)
            if t_expr == None:
                f_parent.addChildren(n_val)
                break
            else:
                f_parent.addChildren(t_expr)
                t_expr.addChildren(n_val)
                f_parent = t_expr          
        return [n2_match]
    elif token['type'] == 'print':    
        return [match(tokens)]#, "print")
    else:
        print("Error Sintáctico other")
        exit()

def stmts(tokens):
    if tokens.peek()['type'] == 'id' or tokens.peek()['type'] == 'print':    
        nodo = stmt(tokens) 
        return nodo + stmts(tokens)
    return []

def dcl(tokens):
    token = tokens.peek()
    if token["type"] == "floatdcl" or token["type"] == "intdcl":
        tmp = token
        tokens.next()

        token = tokens.peek()
        if token['type'] == 'id':
            print(tmp)
            print(token)
            tokens.next()

            return [Nodo(tmp['type'],token['val'])]
        else:
            print("Error sintáctico")
            exit()
    return [] 

def dcls(tokens):
    if tokens.peek()["type"] == "floatdcl" or tokens.peek()["type"] == "intdcl":
        nodo = dcl(tokens)
        return nodo + dcls(tokens)
    return []

def threeAdddressCode(root, since):
    var_tmp = 0
    stmtsChilds = root.children[since:]

    tac = ""
    for stmt in stmtsChilds:
        stack =  []
        curr = stmt
        if (stmt.children):
            while len(curr.children)> 0 :
                stack.append(curr.children[0])
                stack.append(curr)
                stack.append(curr.children[1])
                if len(curr.children[1].children):
                    stack.pop()
                curr = curr.children[1]
        else:
            stack.append(curr)
        
        cont = 0
        sentence = ""        

        while len(stack)>0:
            x = stack.pop()
            if x.type =='print':
                sentence = 'p' +" "+ x.data
                print(sentence)
                tac = tac + sentence+'\n'
            if cont == 3:
                if  x.type != 'assign':
                    stack.append(x)
                    sentence = 'x'+str(var_tmp)+ " = " + sentence
                    cont = 0
                    tac = tac + sentence+'\n'
                    print(sentence)
                    sentence = 'x'+str(var_tmp)
                    cont = 1
                    var_tmp  = var_tmp + 1
                    continue
                else:
                    cont = 0 
            
            if x.type == 'fnum' or x.type == 'inum':
                sentence = str(x.data) +' '+ sentence
            else:
                sentence = x.data +' '+sentence
                if '=' in sentence and not sentence[0] == '=': 
                    print(sentence)
                    tac = tac + sentence+'\n'

            cont = cont + 1
    with open('TAC.txt', 'w') as f:
        f.write(tac)

def visualizeTree(root):
    stmtsChilds = root.children
    v_root = Node("Prog")

    for i in stmtsChilds:
        c_node = Node(i.type + " " +i.data,v_root)
        if len(i.children)==2:
            visualizeTreeNode(i.children[0],i.children[1],c_node)
        if len(i.children)==1: 
            visualizeTreeNode(i.children[0], None ,c_node)
    for pre, fill, node in RenderTree(v_root):
        print("%s%s" % (pre, node.name))
        
def visualizeTreeNode(firstChildren, SecondChildren, N_parent):
    if firstChildren != None:

        fc = Node(firstChildren.type + " " + firstChildren.data,N_parent)
        if len(firstChildren.children)==2:
            visualizeTreeNode(firstChildren.children[0],firstChildren.children[1],fc)
        elif len(firstChildren.children)==1: 
            visualizeTreeNode(firstChildren.children[0], None, fc)
    if SecondChildren != None:
        fc = Node(SecondChildren.type + " " +SecondChildren.data,N_parent)
        if len(SecondChildren.children)==2:
            visualizeTreeNode(SecondChildren.children[0], SecondChildren.children[1], fc)
        elif len(SecondChildren.children)==1: 
            visualizeTreeNode(SecondChildren.children[0], None, fc)
      


# 1 Prog -> Dcls Stmts $
def prog(tokens):
    root = Nodo('prog', None)

    root.addChildren(dcls(tokens))
    x =len(root.children)
    print(x)
    st_tokens = stmts(tokens)
    root.addChildren(st_tokens)
    print(len(root.children))

    threeAdddressCode(root, x)
    visualizeTree(root)
    
with open('input.txt') as f:
    lines = f.read()

tokens = Tokens()
while not eof():
    # Converts the input program into a sequence of Tokens
    tokens.append(scanner())
tokens.append(scanner())

prog(tokens)