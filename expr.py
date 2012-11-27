import re, string, math
from utils import Stack
from utils import Queue

class Operator(object):
    '''This is abstract class representing general concept of operator'''
    def evaluate(self):
        return self.result

class ConstantOperator(Operator):
    '''This is abstract class, subclass of Operator representing general concept of constant operator'''
    def __init__(self, operand):
        self.result = float(operand)

class PiOperator(ConstantOperator):
    '''This is sublass of ContantOperator representing constant operator Pi'''
    def __init__(self, operand):
        self.result = math.pi

class EOperator(ConstantOperator):
    '''This is sublass of ContantOperator representing constant operator e'''
    def __init__(self, operand):
        self.result = math.e

class VariableOperator(ConstantOperator):
    def __init__(self, variable):
        self.result = float(variable)

class InfixOperator(Operator):
    '''This is subclass of Operator representing general concept of binary operator'''
    def __init__(self, operand1, operand2):
        self.operand1 = float(operand1)
        self.operand2 = float(operand2)
        
class AdditionOperator(InfixOperator):
    '''This is subclass of InfixOperator representing operation of addition'''
    def __init__(self, operand1, operand2):
        self.operand1 = float(operand1)
        self.operand2 = float(operand2)
        self.result = self.operand1 + self.operand2

class SubtractionOperator(InfixOperator):
    '''This is subclass of InfixOperator representing operation of subtraction'''
    def __init__(self, operand1, operand2):
        self.operand1 = float(operand1)
        self.operand2 = float(operand2)
        self.result = self.operand1 - self.operand2

class MultiplicationOperator(InfixOperator):
    '''This is subclass of InfixOperator representing operation of multiplication'''
    def __init__(self, operand1, operand2):
        self.operand1 = float(operand1)
        self.operand2 = float(operand2)
        self.result = self.operand1 * self.operand2
    
class DivisionOperator(InfixOperator):
    '''This is subclass of InfixOperator representing operation of division'''
    def __init__(self, operand1, operand2):
        self.operand1 = float(operand1)
        self.operand2 = float(operand2)
        self.result = self.operand1 / self.operand2

class PowerOperator(InfixOperator):
    '''This is subclass of InfixOperator representing operation of powering'''
    def __init__(self, operand1, operand2):
        self.operand1 = float(operand1)
        self.operand2 = float(operand2)
        self.result = self.operand1 ** self.operand2

class OperatorFactory(object):
    '''This is factory object to create instances of particular operators'''
    def newOperator(self, token, stack, varMap):
        if token == 'pi':
            return PiOperator('pi')
        elif token == 'e':
            return EOperator('e')
        elif re.match('\d+', token):
            return ConstantOperator(token)
        elif re.match('[a-z]', token):
            return VariableOperator(varMap[token])
        elif token == '+':
            return AdditionOperator(stack.pop(), stack.pop())
        elif token == '-':
            v2 = stack.pop()
            v1 = stack.pop()
            return SubtractionOperator(v1, v2)
        elif token == '*':
            return MultiplicationOperator(stack.pop(), stack.pop())
        elif token == '/':
            v2 = stack.pop()
            v1 = stack.pop()
            return DivisionOperator(v1, v2)
        elif token == '^':
            v2 = stack.pop()
            v1 = stack.pop()
            return PowerOperator(v1, v2)

class Rpn(object):
    def __init__(self, infix):
        self.infix = re.split('\s*([+\-*/()]|\d+\.\d+|\d+)\s*', infix)
        self.precedence = {'^': (3, 'R'), '*': (2, 'L') ,'/': (2, 'L'), '+': (1, 'L'), '-': (1, 'L')}
        self._rpn = ''
        self.result = 0
        self.mapVariables = {}
     
    def rpn(self):
        return self._rpn
     
    def infix(self):
        return self.infix
     
    def convert(self, verbose):
        self.verbose = verbose
        operators = '^*+-\/'
        #operands = string.ascii_lowercase + string.digits
        output = Queue()
        stack = Stack()
        
        for token in self.infix:
            operands = re.match('^[a-z]$|^\d+\.\d+$|^\d+$', token)
            operators = re.match('^[+-\/*^]$', token)
            # if token is a number or variable add it to putput
            if operands:
                output.push(token)
                if self.verbose == True:
                    print "1 token = %s, output = %s" % (token, output.list[::-1]) 
                # if the token is variable add it mapVariable dictionary 
                if token in string.ascii_lowercase:
                    self.mapVariables[token] = ''
            #if token is an operator
            elif operators:
                # while there is another operator on the stack
                while not stack.isEmpty():
                    # if operator is lef-associative and its precedence is less than or equal to that on stack, or operator has precedence less than that on stack (is not left-associative)
                    if stack.lastOnStack() != '(' and ((self.precedence[token][0] <= self.precedence[stack.lastOnStack()][0] and self.precedence[token][1] == 'L') or self.precedence[token][0] < self.precedence[stack.lastOnStack()][0]):
                        # push operator to output from stack
                        output.push(stack.pop())
                        if self.verbose == True:
                            print "2 token = %s, output = %s" % (token, output.list[::-1]) 
                    else:
                        break
                # push operator to stack
                stack.push(token)
                if self.verbose == True:
                    print "3 token = %s, stack = %s" % (token, stack.list[::-1]) 
            # if token is left parenthesis push it to stack
            elif token == '(':
                stack.push(token)
                if self.verbose == True:
                    print "4 token = %s, stack = %s" % (token, stack.list[::-1]) 
            # if token is right parenthesis 
            elif token == ')':
                # until token at the top of stack is not left parethesis
                while stack.lastOnStack() != '(':
                    # push from stack to output
                    output.push(stack.pop())
                    if self.verbose == True:
                        print "5 token = %s, output = %s" % (token, output.list[::-1]) 
                # and pop left parethesis from stack but not to output
                stack.pop()
        if self.verbose == True:
            print "Left on stack "+str(stack.list[::-1])
            print "Output "+str(output.list)
        self._rpn = output.list[::-1]
        while len(stack.list) > 0:
            self._rpn.append(stack.pop())
        if self.verbose == True:
            print "RPN value = " + str(self._rpn)
        return self._rpn
    
    def evaluate(self, vars):
        stack = Stack()
        queue = Queue()
        for elem in self._rpn:
            factory = OperatorFactory()
            operator = factory.newOperator(elem, stack, vars)
            if self.verbose == True:
                print elem, operator.evaluate()
            stack.push(operator.evaluate())
            if self.verbose == True:
                print stack.s()
        return stack.popAll()

def main(str):    
    
    stack = Stack()
    queue = Queue()
    vars = {'x': 18}
    exp = Rpn(s2)
    rpn = exp.convert(False)
    res = exp.evaluate(vars)
    print res

if __name__ == '__main__':
    s1 = '(2+3)*5'
    s2 = '((2+x)/3^2+(14-3)*4)/2'
    main(s2)


