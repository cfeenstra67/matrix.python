from matexceptions import MatrixException

def emptyListWithSize(size=0):
    result=list()
    for i in range(0,size):
        result.append(None)
    return result
def listOfSizeWithElements(originallist,size):
    resultlist=list(originallist)
    if size==len(originallist):
        return resultlist
    elif size>len(originallist):
        resultlist.extend(emptyListWithSize(size-len(originallist)))
        return resultlist
    else:
        return resultlist[0:size]
def matrixWithRows(*rows, numcols=None):
    """Including a value for numcols will create a matrix with that many columns.  Defaults to
    matrix with number of columns corresponding to the max number of items included in one of the rows"""
    number_of_columns=0
    if numcols is None:
        for item in rows:
            if len(item)>number_of_columns:
                number_of_columns=len(item)
    else:
        number_of_columns=numcols
    new=Matrix(columns=number_of_columns)
    for row in rows:
        new.addRow(row)
    return new
def matrixWithColumns(*columns, numrows=None):
    """see matrixWithRows documentation"""
    mat=MatrixWithRows(*columns,numrows)
    mat.transpose()
    return mat
def checkComparableToMatrix(value):
    if not isinstance(value, Matrix):
        raise MatrixException('comparing other data types to matrices is not defined')

class Matrix:
    """Note: the matrix constructor provided does not allow the programmer to provide data, only
    the number of rows and columns they'd like for the matrix to be.  A good way to declare a matrix
    with its data would be 'mat=Matrix(2,2).input(1,2,3,4).' For matrices, I prefer this initialization
    pattern to one where the constructor argument is the data to be included in the matrix."""
    def __init__(self, rows=0, columns=0):
        self.__rowlist=list()
        self.__columnCount=0
        for i in range(0,rows):
            self.addRow()
        for i in range(0, columns):
            self.addColumn()
    def __len__(self):
        """The length of a matrix returns the total number of elements"""
        return self.size()
    def size(self):
        return len(self.__rowlist)*self.__columnCount
    def __getitem__(self, key):
        """If an integer is passed as the key, __getitem__ will return the row corresponding
        to the key passed.  If a list of length one is passed (effectively using double braces [[]]
        as opposed to normal element access []), __getitem__ will return the column corresponding to
        element passed in a list"""
        if isinstance(key, list) and len(key)==1:
            return self.columnAtIndex(key[0])
        else:
            return self.rowAtIndex(key)        
    def __setitem__(self, key, value):
        if isinstance(key, list) and len(key)==1:
            self.setColumn(key[0],value)
        else:
            self.setRow(index=key, row=value)
    def __str__(self):
        if len(self.__rowlist)==0:
            return 'None'
        myString=''
        for position, row in enumerate(self.__rowlist):
            myString=myString+str(row)
            if position!=len(self.__rowlist)-1:
                myString=myString+'\n'
        return myString
    def __eq__(self, other):
        checkComparableToMatrix(other)
        if other.numrows()!=self.numrows() or other.numcolumns()!=self.numcolumns():
            return False
        same=True
        for myrow, theirrow in zip(self.rows(),other.rows()):
            for myitem, theiritem in zip(myrow, theirrow):
                try:
                    if myitem!=theiritem:
                        same=False
                        break
                except:
                    same=False
                    break
            if not same:
                break
        return same
    def __ne__(self, other):
        return not self.__eq__(other)
    def copy(self):
        newinst=Matrix(columns=self.__columnCount)
        for row in self.__rowlist:
            newinst.addRow(row)
        return newinst
    def isSquare(self):
        return self.numrows()==self.numcolumns()
    def rows(self):
        return self.__rowlist
    def numrows(self):
        return len(self.rows())
    def columns(self):
        copy=self.copy()
        copy.transpose()
        return copy.__rowlist
    def numcolumns(self):
        return int(self.__columnCount)
    def push(self):
        self.addRow()
        self.addColumn()
        return self
    def pop(self, index=-1):
        self.popRow(index)
        self.popColumn(index)
        return self
    def addRow(self, row=None):
        if row==None:
            newRow=emptyListWithSize(self.__columnCount)
            self.__rowlist.append(newRow)
        elif len(row) is self.__columnCount:
            if isinstance(row, list):
                self.__rowlist.append(row)
            else:
                self.__rowlist.append(list(row))
        else:
            newRow=listOfSizeWithElements(list(row),self.__columnCount)
            self.__rowlist.append(newRow)
        return self
    def popRow(self, index=-1):
        row=self[index]
        if len(self.__rowlist)>0:
            self.__rowlist.pop(index)
        else:
            raise MatrixException('minimum number of rows is 0')
        return row
    def popColumn(self, index=-1):
        col=self[[index]]
        if self.__columnCount>0:
            for row in self.__rowlist:
                row.pop(index)
            self.__columnCount-=1
        else:
            raise MatrixException('minimum number of columns is 0')
        return col
    def addColumn(self, column=None):
        self.__columnCount+=1
        if(column==None):
            for row in self.__rowlist:
                row.append(None)
        else:
            newCol=listOfSizeWithElements(column, self.numrows())
            for item, row in zip(newCol,self.__rowlist):
                row.append(item)
        return self
    def insertRow(self,index,row=None):
        if index==self.numrows():
            self.addRow(row)
            return
        bottom=self.splitAtRow(index)
        self.addRow(row)
        self.rbind(bottom)
    def insertColumn(self, index, column=None):
        if index==self.numcolumns():
            self.addColumn(column)
            return
        right=self.splitAtColumn(index)
        self.addColumn(column)
        self.cbind(right)
    def setRow(self, index, row=None):
        newRow=list()
        if row==None:
            newRow=emptyListWithSize(self.__columnCount)
        else:
            newRow=listOfSizeWithElements(list(row),self.__columnCount)
        self.__rowlist[index]=newRow
        return self
    def setColumn(self, index, column=None):
        if column==None:
            for row in self.__rowlist:
                row[index]=None
        else:
            newCol=listOfSizeWithElements(list(column),len(self.__rowlist))
            for item, row in zip(newCol,self.__rowlist):
                row[index]=item
        return self
    def rowAtIndex(self,index):
        return self.rows()[index]
    def columnAtIndex(self, index):
        col=list()
        for row in self.__rowlist:
            col.append(row[index])
        return col
    def switchRows(self, index1, index2):
        self[index1],self[index2]=self[index2],self[index1]
        return self
    def transpose(self):
        numrows=len(self.__rowlist)
        newRows=list()
        for i in range(0,self.__columnCount):
            newRows.append(self[[i]])
        self.__rowlist=newRows
        self.__columnCount=numrows
        return self
    def rbind(self, matrix):
        for row in matrix.rows():
            self.addRow(row)
        return self
    def cbind(self, matrix):
        for col in matrix.columns():
            self.addColumn(col)
        return self
    def reverseRows(self):
        for col in reversed(self.columns()):
            self.addColumn(col)
        for i in range(0,int(self.numcolumns()/2)):
            self.popColumn(0)
        return self
    def reverseColumns(self):
        for row in reversed(self.rows()):
            self.addRow(row)
        for i in range(0,int(self.numrows()/2)):
            self.popRow(0)
        return self
    def splitAtRow(self, index):
        ret=type(self)(columns=self.numcolumns())
        for position, row in enumerate(self.rows()[index:]):
            ret.addRow(row)
        for i in range(0,ret.numrows()):
            self.popRow()
        return ret
    def splitAtColumn(self, index):
        ret=type(self)(rows=self.numrows())
        for position, col in enumerate(self.columns()[index:]):
            ret.addColumn(col)
        for i in range(0,ret.numcolumns()):
            self.popColumn()
        return ret
    def input(self,*args,vertical=False):
        """Note: this will overrwrite all current data in the matrix (unless the number
        of items passed in args is less than the number of elements in the matrix).  For appending
        data to a matrix, addRow and addColumn should be used."""
        if vertical:
            self.transpose()
        row=0
        column=0
        total=self.numrows()
        subtotal=self.numcolumns()
        for newitem in args:
            if row>=total:
                break
            self[row][column]=newitem
            column+=1
            if column>=subtotal:
                column=0
                row+=1
        if vertical:
            self.transpose()
        return self
            
            
            