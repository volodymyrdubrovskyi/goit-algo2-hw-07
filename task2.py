import random
import timeit
import matplotlib.pyplot as plt
from collections import OrderedDict, Counter
from functools import lru_cache

# Реалізація функції з використанням LRU-кешу
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

# Реалізація Splay Tree
class SplayTreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _zig(self, node):
        parent = node.parent
        if node == parent.left:
            if node.right:
                parent.left = node.right
                node.right.parent = parent
            else:
                parent.left = None
            node.right = parent
        else:
            if node.left:
                parent.right = node.left
                node.left.parent = parent
            else:
                parent.right = None
            node.left = parent
        node.parent = parent.parent
        parent.parent = node
        if node.parent:
            if node.parent.left == parent:
                node.parent.left = node
            else:
                node.parent.right = node
        else:
            self.root = node

    def _zig_zig(self, node):
        parent = node.parent
        grandparent = parent.parent
        self._zig(parent)
        self._zig(node)

    def _zig_zag(self, node):
        self._zig(node)
        self._zig(node)

    def _splay(self, node):
        while node.parent:
            if not node.parent.parent:
                self._zig(node)
            elif (node == node.parent.left) == (node.parent == node.parent.parent.left):
                self._zig_zig(node)
            else:
                self._zig_zag(node)

    def insert(self, key, value):
        node = SplayTreeNode(key, value)
        if not self.root:
            self.root = node
        else:
            current = self.root
            while True:
                if key < current.key:
                    if current.left:
                        current = current.left
                    else:
                        current.left = node
                        node.parent = current
                        break
                elif key > current.key:
                    if current.right:
                        current = current.right
                    else:
                        current.right = node
                        node.parent = current
                        break
                else:
                    current.value = value
                    self._splay(current)
                    return
            self._splay(node)

def fibonacci_splay(n, tree):
    node = tree.root
    while node:
        if node.key == n:
            tree._splay(node)
            return node.value
        elif n < node.key:
            node = node.left
        else:
            node = node.right
    if n < 2:
        value = n
    else:
        value = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, value)
    return value

# Створимо набір чисел Фібоначчі від 0 до 950 з кроком 50
fib_numbers = list(range(0, 951, 50))

# Вимірювання часу для fibonacci_lru
times_lru = []
for n in fib_numbers:
    time = timeit.timeit(lambda: fibonacci_lru(n), number=10)
    times_lru.append(time / 10)  # середній час виконання

# Вимірювання часу для fibonacci_splay
times_splay = []
tree = SplayTree()
for n in fib_numbers:
    time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=10)
    times_splay.append(time / 10)  # середній час виконання

# Побудова графіка
plt.plot(fib_numbers, times_lru, label='LRU Cache')
plt.plot(fib_numbers, times_splay, label='Splay Tree')
plt.xlabel('n')
plt.ylabel('Середній час виконання (секунди)')
plt.legend()
plt.show()

# Виведення текстової таблиці
print(f"{'n':>10} {'LRU Cache Time (s)':>20} {'Splay Tree Time (s)':>20}")
for n, t_lru, t_splay in zip(fib_numbers, times_lru, times_splay):
    print(f"{n:>10} {t_lru:^20.8f} {t_splay:^20.8f}")
