import csv
import os
from pathlib import Path

from .models import Member, Account


class Row:
    '''Local Class used by Parser below'''
    def __init__(self, first_name, last_name, phone_number, client_member_id, account_id):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.client_member_id = client_member_id
        self.account_id = account_id


class Parser:
    '''Parser for Member Files in CSV format
       It is a best-effort parser, i.e. it won't stop if a line is formatted incorrectly
       A line should be a tuple of ( id, firstname, lastname, phone number, member ID, account ID )
    '''
    def __init__(self, file_name):
        self.file_name = file_name


    def format_row(self, row):
        '''Attempts to parse a single row'''
        try:
            if len(row) != 6:
                raise ValueError(f"Expecting 6 comma separated input columns: {row}")

            # the ID is ignored as we want to find duplicates
            fname = row[1]
            lname = row[2]
            phone = int(row[3])
            cmember_id = int(row[4])
            acc_id = int(row[5])
            return Row(fname, lname, phone, cmember_id, acc_id)
        except Exception as exc:
            print(f"A parsing error {exc} was caused by \"{row}\", moving on...")
            return None


    def process_csv(self, fname):
        '''Processes a local CSV file '''
        BASE_DIR = Path(__file__).resolve().parent.parent
        fname = os.path.join(BASE_DIR, 'media', fname)
        with open(fname) as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            # 893, Ollie, Capstack, 9050093979, 3807423, 18
            for row in reader:
                data = self.format_row(row)
                if not data:
                    continue

                print(data)

                members = Member.objects.filter(first_name=data.first_name, last_name=data.last_name, phone_number=data.phone_number,
                                                client_member_id=data.client_member_id)
                if not members:
                    member = Member(first_name=data.first_name, last_name=data.last_name, phone_number=data.phone_number,
                                                client_member_id=data.client_member_id)
                    member.save()
                    # create member account mapping
                    memberAccount = Account(member=member, account_id=data.account_id)
                    memberAccount.save()
                    print(f"Saved new member {member}")