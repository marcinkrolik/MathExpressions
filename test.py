import re
from utils import Stack
from utils import Queue

def recu(s, out, stk):
    print s
    for token in s:
        print token
        dig = re.match('\d+', token)
        oper = re.match('[\+\-\/\*]', token)
        if token == '(':
            a = s[s.index(token)+1:s.index(')')]
            print "obciachane ", a
            del s[s.index(')')]
            recu(a, out, stk)
        elif dig:
            out.push(token)
        elif oper:
            stk.push(token) 

output = Queue()
stack = Stack()
s1 = '(2+3)*5'
s2 = re.split('\s*([+\-*/()]|\d+\.\d+|\d+)\s*', s1)
recu(s2, output, stack)
print output.popAll(), stack.popAll()