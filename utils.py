class Stack(object):
    def __init__(self):
        self.list = []
        self.output = ''
 
    def push(self,item):
        self.list.append(item)
 
    def pop(self):
        return self.list.pop()
 
    def isEmpty(self):
        return len(self.list) == 0
   
    def popAll(self):
        while len(self.list) > 0:
            self.output += str(self.pop())
        return self.output
   
    def lastOnStack(self):
        try:
            return self.list[-1]
        except IndexError:
            return False
    
    def s(self):
        return self.list

class Queue(object):
    def __init__(self):
        self.list = []
        self.output = ''
   
    def push(self,item):
        self.list.insert(0,item)
 
    def pop(self):
        return self.list.pop()
 
    def isEmpty(self):
        return len(self.list) == 0
   
    def popAll(self):
        while len(self.list) > 0:
            self.output += self.pop()
        return self.output