class Ref:
    def __init__(self, obj):
       self.obj = obj
    
    def get(self):    
        return self.obj
    
    def set(self, obj):
        self.obj = obj