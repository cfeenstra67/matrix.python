def real(num):
    try:
        return float(num)
    except(ValueError, TypeError):
        return float(0)

class RList(list):
    def __init__(self, iter=None):
        if iter is None:
            return
        for item in iter:
            self.append(item)
    def __setitem__(self, key, value): 
        super(RList, self).__setitem__(key, real(value))
    def append(self, item):
        super(RList, self).append(real(item))
    def extend(self, *iter):
        for item in iter:
            self.append(item)
    
        
