#!/usr/bin/env python3

import connexion
from swagger_server.encoder import JSONEncoder
import os,sys
sys.path.append('./WasonQA')
print(__name__)
app = connexion.App(__name__, specification_dir='./swagger_server/swagger/')
app.app.json_encoder = JSONEncoder
app.add_api('swagger.yaml', arguments={'title': 'QA like Waston'})
application=app.app

if __name__ == '__main__':
    app.run(port=12001,server='tornado')
