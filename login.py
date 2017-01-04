#!/usr/bin/env python
import time
import base64
import argparse
import getpass
import os.path

FILENAME = 'logins.dat'


def listAccounts():
    with open(FILENAME, 'rb') as store_file:
        store_line = store_file.readline()
        while store_line != b'':
            user, password = base64.b64decode(
                store_line).decode('utf8').split(',')
            print('User: {}\t Password: {}'.format(user, password))
            store_line = store_file.readline()


def storeAccount(email, password):
    with open(FILENAME, 'ab') as store_file:
        store_line = '{},{}'.format(email, password)
        store_line = base64.b64encode(store_line.encode('utf8'))
        store_file.write(store_line)
        store_file.write(b'\n')


def main():
    log = argparse.ArgumentParser(description='Storing accounts.')
    log.add_argument("-s", '--store', action="store_true", dest="store",
                     help="save account")
    log.add_argument("-l", '--list', action="store_true", dest="list",
                     help="list saved accounts")

    args = log.parse_args()
    if args.store:
        user = input('Email or username: ')
        password = getpass.getpass('Password: ')
        while password != getpass.getpass('Password (again): '):
            print('Sorry, try again')
            pass
        storeAccount(user, password)
    if args.list:
        listAccounts()


if __name__ == '__main__':
    if not os.path.isfile(FILENAME):
        open(FILENAME, 'wb')
    main()
