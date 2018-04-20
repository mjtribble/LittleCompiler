class MyStack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         if self:
            return self.items[len(self.items)-1]
         else:
            print("Stack is empty")

     def size(self):
         return len(self.items)

     def pretty(self):
         for item in self.items:
             print("Parent: " )
             item.pprint()
             print("Left Child")
             if item.leftChild != None:
                item.leftChild.pprint()
             else:
                 print("No Left Child")
             print("Right Child ")
             if item.rightChild != None:
                item.rightChild.pprint()
             else:
                 print("No Right Child")
         print("End of Current Stack")