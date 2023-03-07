from API_Funcs import get_OAuth_Tokens, Access_Token
import simple_sql
import logging
logging.basicConfig(level=logging.DEBUG)

def main():
    # automation of the 3-legged OAuth process for getting more permanent tokens for a user (at least as much as I could automate the process)
    COLUMNS = []
    DATA = []
    OAuth_Tokens = get_OAuth_Tokens()
    User_OAuth_Tokens = Access_Token(OAuth_Tokens)
    for key in User_OAuth_Tokens:
        COLUMNS.append(key)
        DATA.append(str(User_OAuth_Tokens[key]))
    print("Use this SQL statement to insert the data into the User_OAuth_Info table: " + simple_sql.create_row('twitter_info.User_OAuth_Info', COLUMNS, DATA))
        
if __name__ == '__main__':
    main()