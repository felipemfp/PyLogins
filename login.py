#!/usr/bin/env python
import time
import argparse
import getpass
import os.path
from hashids import Hashids

FILENAME = 'logins.dat'


def encipher(text, secret):
    return Hashids(salt=secret).encode(*(int(c) for c in text.encode('utf8')))


def decipher(cipher, secret):
    return bytes(Hashids(salt=secret).decode(cipher)).decode('utf8')


def list_accounts(secret):
    with open(FILENAME, 'r') as store_file:
        store_line = store_file.readline()
        while store_line != '':
            stored = decipher(store_line[:-1], secret)
            if stored != '':
                user, password = stored.split(',')
                print('User: {}\t Password: {}'.format(user, password))
            store_line = store_file.readline()


def store_account(secret, email, password):
    with open(FILENAME, 'a') as store_file:
        store_line = '{},{}'.format(email, password)
        store_line = encipher(store_line, secret)
        store_file.write('{}\n'.format(store_line))


def main():
    log = argparse.ArgumentParser(description='Storing accounts.')
    log.add_argument("-s", '--store', action="store_true", dest="store",
                     help="save account")
    log.add_argument("-l", '--list', action="store_true", dest="list",
                     help="list saved accounts")

    args = log.parse_args()
    secret = getpass.getpass('Secret: ')
    if args.store:
        user = input('Email or username: ')
        password = getpass.getpass('Password: ')
        while password != getpass.getpass('Password (again): '):
            print('Sorry, try again')
            pass
        store_account(secret, user, password)
    if args.list:
        list_accounts(secret)


if __name__ == '__main__':
    if not os.path.isfile(FILENAME):
        open(FILENAME, 'wb')
    main()
