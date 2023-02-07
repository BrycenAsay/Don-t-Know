def create_table(table_name, columns, data_types):
    query = ["""CREATE TABLE """]
    query.append(f'{table_name}(')
    for i in range(len(columns) - 1):
        query.append(f'{columns[i]} {data_types[i]},')
    query.append(f'{columns[-1]} {data_types[-1]});')
    return '\n'.join(query)

def create_row(table_name, columns, data):
    columns = ','.join(columns)
    data = ','.join(data)
    query = f'INSERT INTO {table_name}({columns}) VALUES ({data});'
    return query

colms = ['tweet_id', 'body', 'likes', 'views', 'created_on']
datatypes = ['int', 'text', 'int', 'int', 'datetime']