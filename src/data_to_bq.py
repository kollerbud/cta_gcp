import sqlite3
from pathlib import Path
from typing import List, Dict

class StoreToDB:
    '''
        contains all database operation
        may expand to cloud db later
    '''
    
    def __init__(self) -> None:
        
        self.cur = sqlite3.connect('rawData/cta.db')
        self.build_table()


    def build_table(self) -> None:
        
        sql_statement = ''' 
            CREATE TABLE IF NOT EXISTS division_stop (
                    staNm TEXT,
                    stpDe TEXT,
                    rn INTEGER,
                    prdt TEXT,
                    arrT TEXT,
                    isApp INTEGER,
                    isSch INTEGER,
                    isDly INTEGER,
                    resp_time TEXT
        )
        '''
        self.cur.execute(sql_statement)
    
    def upload_to_table(self, data: List[Dict]) -> None:
        
        sql_statement = '''
            INSERT INTO division_stop(
                staNm, stpDe, rn, prdt, arrT, isApp, isSch, isDly, resp_time
            )
            VALUES(?,?,?,?,?,?,?,?,?)
        '''
        
        for d in data:
            self.cur.execute(sql_statement, (d['staNm'], d['stpDe'], d['rn'], d['prdt'],
                                             d['arrT'], d['isApp'], d['isSch'], d['isDly'], d['resp_time'])
                             )
        self.cur.commit()

    def nuke(self) -> None:
        '''
        option to wipe local database
        '''
        
        sql_statement ='''
            DELETE FROM division_stop;
        '''
        self.cur.execute(sql_statement)
        self.cur.commit()
        

if __name__ == '__main__':
    StoreToDB().nuke()