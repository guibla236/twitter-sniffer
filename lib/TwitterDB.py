class TwitterDataBase:
    def __init__(self,version, date):
        self.fileName=version
        self.tableName=date

    def getTableName(self):
        return(self.tableName)

    def getFileName(self):
        return(self.fileName)

    def setTableName(self,newTableName):
        self.tableName=newTableName

    def setFileName(self,newFileName):
        self.fileName=newFileName

    def setColsName(self,cols):
        self.cols=cols

    def getColsName(self):
        return(self.cols)

    def baseCreator(self,cols=None):
        """Nombre del archivo ".db", nombre de la tabla a buscar
        y nombre de las columnas separadas por coma y entrecomilla,
        ejemplo: '(var1,var2,...)' """
        import sqlite3
        self.conector=sqlite3.connect(self.getFileName()+'.db')
        self.cursor=self.conector.cursor()
        if cols!=None:
            self.tableCreator(self.getTableName(),cols)

    def tableCreator(self,tableName,cols=None):
        if tableName!=self.getTableName():
            self.setTableName(tableName)

        if cols!=None:
            self.setColsName(cols)

        self.getCursor().execute("CREATE TABLE IF NOT EXISTS "+self.getTableName()+"("+self.getColsName()+")")


    def getCursor(self):
        return self.cursor

    def getConector(self):
        return self.conector

    def closeCursor(self):
        self.cursor.close()

    def closeConector(self):
        self.conector.close()
    def insertData(self,col1,col2,col3,col4,col5,col6,col7,col8):
        from datetime import date
        if date.today().strftime("_%d_%m_%Y")!=self.getTableName():
            print("CAMBIO DE DÍA")
            self.tableCreator(date.today().strftime("_%d_%m_%Y"))

        #DEBUG: else:
            #Implementar
            #print("Mismo día")

        self.getCursor().execute("INSERT INTO {} VALUES (?,?,?,?,?,?,?,?)".format(self.getTableName()),
                    (col1,col2,col3,col4,col5,col6,col7,col8))
        self.getConector().commit()
