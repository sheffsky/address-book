#!/usr/bin/python
import shelve
from datetime import datetime

address_db = shelve.open("address.db")


class ContactItem:
    def get_name(self):
        return self.name

    def get_phone(self):
        return self.phone

    def get_birth_date(self):
        return self.birth_date

    def __init__(self, name, phone, birth_date):
        self.name = name
        self.phone = phone
        self.birth_date = birth_date

    def __str__(self):
        return "Name: {0}, Phone: {1}, Birthday: {2}" \
            .format(self.get_name(),
                    self.get_phone(),
                    self.get_birth_date().strftime("%d.%m.%Y")
                    )


def db_list_contacts():
    print "Contacts list:"
    for line in address_db.itervalues():
        print(line)


def db_find_contact():
    text_to_find = raw_input("Enter a contact name you want to find: ")
    found = False
    for line in address_db.itervalues():
        if text_to_find in line.get_name():
            print line
            found = True
    if not found:
        print "Nothing was found."


def db_create_contact():
    full_name = raw_input("Contact full name: ")
    phone = raw_input("Phone number: ")
    birth_date_raw = raw_input("Date of birth (dd.mm.yyyy): ")

    try:
        birth_date = datetime.strptime(birth_date_raw, "%d.%m.%Y")
        new_contact = ContactItem(full_name, phone, birth_date)
        if full_name in address_db:
            if raw_input("There is already such name. Update record? [y/N] ").capitalize() != "Y":
                print "Canceled."
                return

        address_db[full_name] = new_contact
        address_db.sync()
        print ("Done.")
    except ValueError:
        print "Wrong birthday date format!"


def db_delete_contact():
    name = raw_input("Enter an exact name of the contact: ")
    try:
        del address_db[name]
        address_db.sync()
        print ("Done.")
    except KeyError:
        print "Unable to found such contact."


def exit_program():
    print "Bye!"
    exit()


def check_for_birthday():
    for line in address_db.itervalues():
        if line.get_birth_date().strftime("%d.%m") == datetime.now().strftime('%d.%m'):
            print "{0} has a birthday today!".format(line.get_name())


actions = {1: ("List all contacts", db_list_contacts),
           2: ("Create contact", db_create_contact),
           3: ("Find contact", db_find_contact),
           4: ("Delete contact", db_delete_contact),
           5: ("Quit", exit_program)
           }


def print_menu():
    options = actions.keys()
    options.sort()
    for entry in options:
        print entry, actions[entry][0]


check_for_birthday()

while True:
    print_menu()
    answer = raw_input("Choose an option: ")

    try:
        actions[int(answer)][1]()
    except (KeyError, ValueError):
        print "The option you've entered is incorrect."
