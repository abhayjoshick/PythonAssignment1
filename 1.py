class A:
    def __init__(self):
        self.x = 10
obj = A()
obj.x = 20
del obj.x
print(obj.x)