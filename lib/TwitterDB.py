import sqlite3
from datetime import date

class TwitterDataBase:
    def __init__(self, date,cols_names):
        """
        This class creates the database object to use with Twitter Sniffer. 
        The name of the database saved in the path directory is the actual date. 
        When a new day is detected, the DB file changes automatically 
        (when a new row is attached).
        Thanks to this, the only needed parameter to initialize this object
        is the column names that the DB is going to have.
        
        -cols_names is a list of strings who has the cols names desired.
        
        This class has the method insertData. Use this to insert data respecting
        amount of columns defined in this initialization.
        """
        self.fileName=date
        self.tableName="Table1"
        self.setColsNames(",".join(cols_names))
        self.baseCreator(self.getColsNames())
        

    def getTableName(self):
        return(self.tableName)

    def getFileName(self):
        return(self.fileName)

    def setTableName(self,newTableName):
        self.tableName=newTableName

    def setFileName(self,newFileName):
        self.fileName=newFileName

    def setColsNames(self,cols):
        self.cols=cols

    def getColsNames(self):
        return(self.cols)

    def baseCreator(self,newFileName=None,cols=None):
        
        if newFileName:
            self.conector=sqlite3.connect(newFileName+'.db')
            self.setFileName(newFileName)
        
        else:
            self.conector=sqlite3.connect(self.getFileName()+'.db')

        self.cursor=self.conector.cursor()
        self.tableCreator(self.getTableName(),self.getColsNames())
        
    
    def tableCreator(self,tableName):
        if tableName!=self.getTableName(): 
            self.setTableName(tableName)
       
        self.getCursor().execute("CREATE TABLE IF NOT EXISTS "+self.getTableName()+"("+self.getColsName()+")")


    def getCursor(self):
        return self.cursor

    def getConector(self):
        return self.conector

    def closeCursor(self):
        self.cursor.close()

    def closeConector(self):
        self.conector.close()
    
    def insertData(self,cols):
        """
        
        Insert the twit data into the SQLite database.
        
        -cols is a list ordered in the same way that the DB is defined. In example: element 1 of the list is assigned to column 1 of the DB.
        
        If an error occurs, probably there are an error in the number of elements which is passed or the type of element assigned.
        """
        if date.today().strftime("%d_%m_%Y")!=self.getFileName():
            self.closeCursor()
            self.closeConector()
            self.baseCreator(date.today().strftime("%d_%m_%Y"))
        
        data=",".join(cols)
        
        self.getCursor().execute("INSERT INTO {} VALUES (?)".format(self.getTableName()),
                    (data))
        
        self.getConector().commit()
