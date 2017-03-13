from matrix import listOfSizeWithElements, emptyListWithSize, Matrix, matrixWithRows, matrixWithColumns
from rlist import RList, real
from matexceptions import RMatrixArithmeticError

def RListOfSizeWithElements(originallist, size):
    return RList(listOfSizeWithElements(originallist, size))
def emptyRListWithSize(size=0):
    return RList(emptyListWithSize(size))
def scaleRList(rlist,factor=1.0):
    newList=RList()
    for num in rlist:
        newList.append(num*real(factor))
    return newList
def RMatrixWithRows(*rows,numcols=None):
    mat=matrixWithRows(*rows,numcols)
    rmat=RMatrix(columns=mat.numcolumns())
    for row in mat.rows():
        rmat.addRow(row)
    return rmat
def RMatrixWithColumns(*cols,numrows=None):
    return RMatrixWithRows(*cols,numrows).transpose()
    
def columnsolved(column,index):
    if len(column) is 0:
        return True
    nonzeros=0
    for position, num in enumerate(column):
        if num is 0.0:
            pass
        elif position is not index:
            return False
        else:
            nonzeros+=1
    return (nonzeros is 1)
    
def float_equal(a,b):
    return abs(a-b)<=1e-12
    
def allzero(some_list):
    all=True
    for item in some_list:
        if not float_equal(item,0.0):
            all=False
            break
    return all
def allzeromatrix(matrix):
    allzerom=True
    for row in matrix.rows():
        if not allzero(row):
            allzerom=False
    return allzerom
def nonzeroindices(matrix):
    indices=list()
    for position, row in enumerate(matrix.rows()):
        if not allzero(row):
            indices.append(position)
    return indices
def nonzeroitems(iter):
    mat=RMatrix(columns=len(iter))
    mat.addRow(iter)
    return nonzeroindices(mat.transpose())

def passesFirstCondition(matrix):
    nonzeros=nonzeroindices(matrix)
    nonzeros.sort()
    for position, index in enumerate(nonzeros):
        if position is not index:
            return False
    return True
def passesSecondCondition(matrix):
    'This assumes the matrix passes the first condition'
    nonzeros=nonzeroindices(matrix)
    nonzeros.sort()
    maxind=nonzeros[-1]
    farleft=-1
    for row in matrix.rows()[0:maxind+1]:
        firstnonzero=-1
        for pos, num in enumerate(row):
            if not float_equal(num,0.0):
                firstnonzero=pos
                break
        if firstnonzero<=farleft:
            return False
        else:
            farleft=firstnonzero
    return True
def passesBothConditions(matrix):
    if passesFirstCondition(matrix) and passesSecondCondition(matrix):
        return True
    return False           
def forwardReduce(matrix):
    if not isinstance(matrix, RMatrix):
        raise TypeError
    elif allzeromatrix(matrix):
        return matrix
    else:
        if not passesFirstCondition(matrix):
            return forwardReduce(zerorowstobottom(matrix))
        elif not passesSecondCondition(matrix):
            transposedcopy=matrix.copy().transpose()
            nonzerocols=nonzeroindices(transposedcopy)
            first_nonzero=min(nonzerocols)
            nonzeronums=nonzeroitems(matrix[[first_nonzero]])
            matcopy=matrix.copy()
            matcopy.switchRows(0,min(nonzeronums))
            frow=matcopy[0]
            matcopy.popRow(0)
            iteratorcopy=matcopy.copy()
            for position, num in enumerate(iteratorcopy[[first_nonzero]]):
                if not float_equal(num, 0):
                    matcopy.rowAddition(position,frow,-num/(frow[first_nonzero]))
            if matrix.numrows()>1:
                frowmat=RMatrix(columns=len(frow))
                frowmat.addRow(frow)
                return frowmat.rbind(forwardReduce(matcopy))
            else:
                return matrix
        else:
            return matrix
def determinant(matrix):
    """if the matrix is not square, the determinant is not defined.  Therefore, if a non-square matrix
    is passed to this function it will return None"""
    if not matrix.isSquare():
        return None
    elif matrix.size() is 1:
        return matrix[0][0]
    else:
        fullsum=0
        multiplier=1
        workingcopy=matrix.copy()
        workingcopy.popRow(0)
        for position, item in enumerate(matrix[0]):
            smallercopy=workingcopy.copy()
            smallercopy.popColumn(position)
            fullsum+=multiplier*item*determinant(smallercopy)
            multiplier*=-1
        return fullsum

def zerorowstobottom(matrix):
    matcopy=matrix.copy()
    zerorows=0
    for pos, row in enumerate(reversed(matrix.rows())):
        if allzero(row):
            matcopy.popRow(-(pos+1))
            matcopy.addRow(row)
    return matcopy   
def complement(l, universe=None):
    if universe is not None:
        universe=set(universe)
    else:
        universe=set(range(min(l),max(l)+1))
    return sorted(universe-set(l))
def sumRLists(list1, list2):
    sumlist=RList()
    for num1, num2 in zip(list1, list2):
        sumlist.append(num1+num2)
    return sumlist
    
def identityMatrixWithRows(numrows):
    mat=RMatrix(rows=numrows,columns=numrows)
    for i in range(0,numrows):
        mat[i][i]=1
    return mat
def scalePivotsTo1(matrix):
    for position,row in enumerate(matrix.rows()):
        nonzeros=nonzeroitems(row)
        if len(nonzeros)>0:
            matrix.scaleRow(position,1/row[min(nonzeros)])
    
class RMatrix(Matrix):
    def __neg__(self):
        negmat=self.copy()
        for i in range(0,self.numrows()):
            negmat.scaleRow(i,-1)
        return negmat
    def __pos__(self):
        return self
    def __add__(self, othermatrix):
        if not isinstance(othermatrix, RMatrix):
            raise TypeError
        if self.numrows()!=othermatrix.numrows() or self.numcolumns()!=othermatrix.numcolumns():
            raise RMatrixArithmeticError('adding differently sized matrices is undefined')
        summat=RMatrix(columns=self.numcolumns())
        for position, (row1, row2) in enumerate(zip(self.rows(),othermatrix.rows())):
            summat.addRow(sumRLists(row1,row2))
        return summat
    def __sub__(self, othermatrix):
        return self+-othermatrix
    def __mul__(self, other):
        if isinstance(other, RMatrix):
            return self.__matmul__(other)
        scaled=self.copy()
        for i in range(0,self.numrows()):
            scaled.scaleRow(i,other)
        return scaled
    def __matmul__(self, other):
        if not isinstance(other, RMatrix):
            raise TypeError
        if self.numcolumns()!=other.numrows():
            raise RMatrixArithmeticError('attempting to multiply incompatible matrices')
        result=RMatrix(rows=self.numrows(),columns=other.numcolumns())
        for r in range(0,result.numrows()):
            for c in range(0,result.numcolumns()):
                sum=0
                for rowitem, columnitem in zip(self[r],other[[c]]):
                    sum+=rowitem*columnitem
                    result[r][c]=sum
        return result
    def addRow(self, row=None):
        newRow=None
        if row==None:
            newRow=emptyRListWithSize(self.numcolumns())
        else:
            newRow=RListOfSizeWithElements(row,self.numcolumns())
        super().addRow(newRow)
    def columnAtIndex(self, index):
        col=RList()
        for row in self.rows():
            col.append(row[index])
        return col
    def copy(self):
        new=RMatrix(columns=self.numcolumns())
        for row in self.rows():
            new.addRow(row)
        return new
    def setRow(self, index, row=None):
        newRow=None
        if row is None:
            newRow=emptyRListWithSize(self.numcolumns())
        else:
            newRow=RListOfSizeWithElements(list(row), self.numcolumns())
        super().setRow(index, newRow)
    def REform(self):
        return forwardReduce(self)
    def RREform(self):
        """note: if you have an augmented matrix with more than one augmented columns (as with the inverse
        -finding strategy in which you augment a matrix with the identity matrix), you should not use
        this method.  Using REform() will, however, work, so depending on the problem simply getting the
        matrix to Row-Echelon form may be the best approach.  See code of 'inverse' method for an example of
        obtaining RREform from a matrix augmented with another matrix of the same size--essentially,
        it just requires handling the original matrix and the matrix it's augmented with seperately when
        reversing rows and columns"""
        re=self.REform()
        re.reverseRows().reverseColumns()
        re=re.REform()
        scalePivotsTo1(re)
        return zerorowstobottom(re.reverseRows().reverseColumns())
    def determinant(self):
        return determinant(self)
    def rowAddition(self, index, addition, factor=1.0):
        """index determines the row to which addition is being done. addition can either pass
        a numeric iterable containing a row to be added or the index of the row which should be
        added. factor is optional and determines the scale factor to be applied to the row being
        added."""
        copy=RList()
        if not isinstance(addition, list):
            addition=self[addition]
        for num, add in zip(self[index],scaleRList(RListOfSizeWithElements(addition,self.numcolumns()),factor)):
            copy.append(num+add)
        self[index]=copy
    def scaleRow(self, index, factor=1.0):
        self.rowAddition(index,index,factor-1)
    def invertible(self):
        det=self.determinant()
        return det!=0 and det!=None
    def inverse(self):
        if not self.invertible():
            return None
        iden=identityMatrixWithRows(self.numrows())
        both=self.copy().cbind(iden)
        both=both.REform()
        iden=both.splitAtColumn(iden.numcolumns())
        both.reverseRows().reverseColumns()
        iden.reverseRows().reverseColumns()
        both.cbind(iden)
        both=both.REform()
        scalePivotsTo1(both)
        return zerorowstobottom(both.splitAtColumn(iden.numcolumns()).reverseRows().reverseColumns())  