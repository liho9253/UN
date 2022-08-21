import configparser

host = 'https://www.google.com'
port = 88

config = configparser.ConfigParser()
config['http'] = {}
config['http']['host'] = host
config['http']['port'] = str(port)



with open('config.ini', 'w') as f:
    config.write(f)

print(config['http']['host'])

print(config.sections())




# with open('config.ini', 'r') as f:
#     htT1 = f.readlines()[1]
    
# with open('config.ini', 'r') as f:
#     htT2 = f.readlines()[2]


# print(htT1)
# print(htT2)

# with open('config.ini', 'w') as f:
#     config['http']['host'] = htT1
#     config.write(f)