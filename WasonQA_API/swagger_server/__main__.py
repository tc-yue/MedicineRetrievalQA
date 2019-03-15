#!/usr/bin/env python3

import connexion
from .encoder import JSONEncoder
import os,sys
sys.path.append('./WasonQA')

#print(__name__)
app = connexion.App(__name__, specification_dir='./swagger/')
application=app.app
if __name__ == '__main__':
    #app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'QA like Waston'})
    app.run(port=9230,server='tornado')
