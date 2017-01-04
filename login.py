#!/usr/bin/env python
import time
import argparse
import getpass
import os.path
from hashids import Hashids
from tabulate import tabulate

FILENAME = 'logins.dat'
accounts = []


def encipher(text, secret):
    return Hashids(salt=secret).encode(*(int(c) for c in text.encode('utf8')))


def decipher(cipher, secret):
    return bytes(Hashids(salt=secret).decode(cipher)).decode('utf8')


def load_accounts(secret):
    global accounts
    with open(FILENAME, 'r') as store_file:
        for store_line in store_file:
            stored = decipher(store_line[:-1], secret)
            if stored != '':
                accounts += [stored.split(',')]


def list_accounts():
    global accounts
    print(tabulate([account[0:2] for account in accounts],
                   headers=('Application', 'User'), tablefmt="grid"))


def show_account(application, user):
    global accounts
    for account in accounts:
        if account[0] == application and account[1] == user:
            print(tabulate([account[0:2], ],
                           headers=('Application', 'User'), tablefmt="grid"))


def show_account_password(application, user):
    global accounts
    for account in accounts:
        if account[0] == application and account[1] == user:
            input('{}\r'.format(account[2]))


def delete_account(application, user):
    global accounts
    accountToDelete = []
    for account in accounts:
        if account[0] == application and account[1] == user:
            accountToDelete = account
    accounts.remove(accountToDelete)


def store_account(application, user, password):
    global accounts
    accounts += [[application, user, password]]


def store_accounts(secret):
    global accounts
    with open(FILENAME, 'w') as store_file:
        for account in accounts:
            store_line = '{},{},{}'.format(*account)
            store_line = encipher(store_line, secret)
            store_file.write('{}\n'.format(store_line))


def main():
    log = argparse.ArgumentParser(description='Storing accounts.')
    log.add_argument("-s", '--store', action="store_true", dest="store",
                     help="save account")
    log.add_argument("-l", '--list', action="store_true", dest="list",
                     help="list saved accounts")
    log.add_argument('-a', '--application', action="store", dest='application',
                     help='select app\'s account')
    log.add_argument('-u', '--user', action="store", dest='user',
                     help='select user\'s password')
    log.add_argument('-D', '--DELETE', action="store_true", dest='delete',
                    help='delete account')

    args = log.parse_args()
    secret = getpass.getpass('Provide your secret, please: ')
    load_accounts(secret)
    if args.store:
        print('\nAdd a new account\n')
        application = input('Application: ')
        user = input('Email or username: ')
        password = getpass.getpass('Password: ')
        while password != getpass.getpass('Password (again): '):
            print('Sorry, try again')
            pass
        store_account(application, user, password)
    elif args.list:
        print('\nThese are your saved accounts:\n')
        list_accounts()
        print('\nTo see a password: -a application -u user')
    elif args.user and args.application:
        if args.delete:
            print('\nWould you like to delete the following account?')
            show_account(args.application, args.user)
            if input('Yes or no? ').lower() == 'yes':
                delete_account(args.application, args.user)
        else:
            print('\nYou can see you password below (note you should erase it)')
            show_account_password(args.application, args.user)
    store_accounts(secret)


if __name__ == '__main__':
    if not os.path.isfile(FILENAME):
        open(FILENAME, 'wb')
    main()
