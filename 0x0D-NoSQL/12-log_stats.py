#!/usr/bin/env python3
'''
Provide stats about Nginx logs stored in MongoDB
'''
from pymongo import MongoClient


if __name__ == '__main__':
    client = MongoClient('mongodb://localhost:27017').logs.nginx
    print(f'{client.count_documents({})} logs')
    print('Methods:')
    print(f'\tmethod GET: {client.count_documents({"method": "GET"})}')
    print(f'\tmethod POST: {client.count_documents({"method": "POST"})}')
    print(f'\tmethod PUT: {client.count_documents({"method": "PUT"})}')
    print(f'\tmethod PATCH: {client.count_documents({"method": "PATCH"})}')
    print(f'\tmethod DELETE: {client.count_documents({"method": "DELETE"})}')
    print(f'{client.count_documents({"path": "/status"})} status check')
