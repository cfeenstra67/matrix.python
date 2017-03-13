class MatrixException(Exception):
    def __init__(self, text=None):
        self.text=text
    def __str__(self):
        if self.text is None:
            return 'Raised'
        else:
            return self.text
            
class RMatrixException(MatrixException):
    pass
    
class RMatrixArithmeticError(RMatrixException):
    def __init__(self, reason=None):
        self.reason=reason
    def __str__(self):
        reasonstring=self.reason
        if reasonstring is None:
            reasonstring='unspecified'
        return 'reason:'+reasonstring