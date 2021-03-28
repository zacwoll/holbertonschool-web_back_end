#!/usr/bin/env python3
""" Encryption Implementation Module """
# imports
import bcrypt

def hash_password(password: str):
    """ Hashes password and salts it """
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def is_valid(password: str, hashed_pw):
    return bcrypt.checkpw(password.encode('utf8'), hashed_pw)

if __name__ == "__main__":
    password = "MyAmazingPassw0rd"
    hashed = hash_password(password)
    print(hashed)
    print(is_valid(password, hashed))
