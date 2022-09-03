from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# python3环境下需要decode
pw_hash = bcrypt.generate_password_hash('hunter2').decode('utf-8')
print(pw_hash)
# $2b$12$rSXRS7OFI2MmInOB/0tMgelZLCSby3o/okGPpaVUSTl6I2sCX.ogW

ret = bcrypt.check_password_hash('hunter2', pw_hash)
print(ret)
print(len(pw_hash))