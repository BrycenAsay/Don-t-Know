from API_Funcs import get_OAuth_Tokens, Access_Token
from sqlalchemy import create_engine
import pandas as pd
from config import HOST, USER, PASSWORD, DATABASE, _USERNAME
import mysql.connector
import simple_sql
import logging
logging.basicConfig(level=logging.DEBUG)

def main():
    COLUMNS = []
    DATA = []
    OAuth_Tokens = get_OAuth_Tokens()
    User_OAuth_Tokens = Access_Token(OAuth_Tokens)
    for key in User_OAuth_Tokens:
        COLUMNS.append(key)
        DATA.append(User_OAuth_Tokens[key])
    print([simple_sql.create_row('twitter_info.User_OAuth_Info', COLUMNS, DATA)])

def another_main():
    engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')
    User_Auth = pd.DataFrame()
    with engine.connect() as conn:
        User_Auth = (pd.read_sql_table('User_OAuth_Info', conn)).to_dict()
        print(User_Auth)

"""
    conn = mysql.connector.connect(user=f'{USER}', password=f'{PASSWORD}', host=f'{HOST}', database=f'{DATABASE}')
    with conn.cursor() as cursor:
        sql = simple_sql.create_row('twitter_info.User_OAuth_Info', COLUMNS, DATA)
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            logging.exception('Did not work')
            conn.rollback()
        
        conn.close()
"""
        
if __name__ == '__main__':
    another_main()