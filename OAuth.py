from API_Funcs import get_OAuth_Tokens, Access_Token

def main():
    OAuth_Tokens = get_OAuth_Tokens()
    User_OAuth_Tokens = Access_Token(OAuth_Tokens)
    print(User_OAuth_Tokens)

if __name__ == '__main__':
    main()