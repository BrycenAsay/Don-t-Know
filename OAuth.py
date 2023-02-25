from API_Funcs import get_OAuth_Tokens

def main():
    OAuth_Tokens = get_OAuth_Tokens()
    print(OAuth_Tokens)

if __name__ == '__main__':
    main()