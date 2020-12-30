import os
from twilio.rest import Client
import pandas as pd
from datetime import date, datetime
import schedule
import time

# connect to addressBook.csv
user_info = pd.read_csv('addressBook.csv')

fn = 'Tamara'
ln = 'Spivey'
pn = '907-434-1747'


# either manually input information
account_sid = "<account_sid_goes_here>"
auth_token = "<auth_token_goes_here>"

# or use environmental variables to set it up
# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']

twilio_number = '+15153254937'


client = Client(account_sid, auth_token)

'''
I've set the program to run regardless of the day of the month
for testing purposes, otherwise the program would run everyday until the 1st
to send the message to the correctly formatted numbers
you can change to the scheduled version by switching the function calls
in the main function at the bottom
'''

#scheduled message for the first of the month
#you can use these by switching out the function calls in the main function
def scheduled_message():
    # python schedule does not have a monthly option
    # check each day if it is the 1st of the month
    schedule.every().day.at("00:00").do(monthly_message)
    while 1:
        schedule.run_pending()
        time.sleep(1)

def monthly_message():
    #check if it is the 1st
    if date.today().day != 1:
        return
    else:
        send_messages()

    #parameter: date -> format: month/day/year
#return Boolean True or False
def check_valid_date(date):
    #split date to month - day - year
    x = str(date).split("/", 2)
    correctDate = None
    try:
        # format: datetime(year, month, day)
        newDate = datetime(int(x[2]), int(x[0]), int(x[1]))
        correctDate = True
    except ValueError:
        correctDate = False
    return correctDate


# using either time date function or hardcode any month (1-12)
# return pair information
# pair -> first name and number
def find_verfied_users():
    current_month = date.today().month
    contact_list = []
    #check to see if any users month matches the current month

    for dates in user_info['Date of Birth']:
        #check for any missing values)
        if dates == 'nan':
            break
        #split the month from the date and check with current month
        else:
            x = str(dates).split("/", 1)
            if x[0] == str(current_month):
                # we must verify the rest of the date
                check = check_valid_date(dates)
                if check == True:
                    #get First Name and Mobile Phone
                    phone = user_info[user_info['Date of Birth']==dates]['Mobile Phone'].values
                    first_name = user_info[user_info['Date of Birth']==dates]['First Name'].values
                    #skip any names with no mobile number
                    if str(phone[0]) != 'nan':
                        contact_list.append([first_name[0],int(phone[0])])
    return contact_list

def send_messages():
    contact_list = find_verfied_users()
    for contacts in contact_list:
        # assumes US number
        number = ('+1' + str(contacts[1]))
        body_message = 'Happy Birthday %s from %s %s! Call me at %s to plan a lunch sometime.' % (str(contacts[0]), fn,
                                                                                                  ln, pn)
        client.messages.create(
            body=body_message,
            from_=twilio_number,
            to=number
        )


if __name__ == "__main__":
    send_messages()
    #scheduled_message()