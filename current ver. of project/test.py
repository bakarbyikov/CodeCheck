from re import L
import math

class Node:
    def __init__(self, value = None, left = None, right = None):
      self.value = value
      self.left = left
      self.right = right
    def value(self):
      return self.value
    def print_node(self):
      print(f"this node {self.value} has\nthe left son = {self.left} and the right son {self.right}")


class Balanced_tree:
  def __init__(self, root = None):
    self.root = root

  def build_balanced_tree(self, arr):
    if len(arr) == 0:
      return
    self.root = Node(value = arr[0])
    #пробежка по этажам
    for i in range(1, math.ceil(math.log2(len(arr)))):
      #print(f"It's level {i}")
      a = []
      b = []
      for n in range(2**(i-1) - 1, 2**i - 1):
        a.append(Node(value = arr[n]))
      for j in range(2**i-1, 2**(i+1)-1):
        if j < len(arr):
          b.append(Node(value = arr[j]))
      if len(b) % 2 == 0:
        for x, y1, y2 in zip(a, b[::2], b[1::2]):
          #print(x.value, y1.value, y2.value)
          if self.root.value == x.value:
            self.root.right = y1
            self.root.left = y2
          self.root = x
      else:
        c = []
        for k in b[1::2]:
          c.append(k)
        c.append(None)
        for x, y1, y2 in zip(a, b[::2], c):
          #print(x.value, y1.value, y2.value)
          if self.root.value == x.value:
            self.root.right = y1
            self.root.left = y2
          self.root = x
  def print_tree(self):
    print(self.root.value)

arrr = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]

#чтение файла основано для такого file.txt, в котором ноды хранятся по порядку без раздели
#f = open('/content/nodes.txt', 'r').read()
#a = []
#for i in range(len(f)):
#  a.append(int(f[i]))

bt = Balanced_tree(root = Node(value = 2))
#bt.build_balanced_tree(arr = arrr)
bt.print_tree
print(6*0.383**2*0.3085**2)