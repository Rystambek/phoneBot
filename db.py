from tinydb import TinyDB, Query

class DB:
    def __init__(self,path):
        self.db = TinyDB(path)

    def get_tables(self):
        """
        To get the list of all the tables in the database
        """
        return list(self.db.tables())
        
    def getPhone(self,brand,idx):
        """
        Return phone data by brand
        args:
            brand: str
        return:
            dict
        """
        table = self.db.table(brand)
        return table.get(doc_id=idx)

    def get_phone_list(self,brand):
        """
        Return phone list
        """
        table = self.db.table(brand)
        return table.all()

        

# db = DB('db.json')
# tables = db.get_tables()
# print(tables)
# print(db.get_phone_list(tables[0]))