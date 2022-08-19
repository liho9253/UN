import configparser

host = 'https://www.google.com'
port = 88

config = configparser.ConfigParser()
config['http'] = {}
config['http']['host'] = host
config['http']['port'] = str(port)



with open('config.ini', 'r') as f:
    print(f.readlines()[2])
    print(f.readlines()[0])
    