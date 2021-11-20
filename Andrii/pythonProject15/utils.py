
import datetime

import yagmail


def phrase_timetable(table):
    weekday = datetime.datetime.today().weekday()
    if weekday == 0:
        return f'your schedule for today is {table["monday"]}'
    if weekday == 1:
        return f'your schedule for today is {table["tuesday"]}'
    if weekday == 2:
        return f'your schedule for today is {table["wednesday"]}'
    if weekday == 3:
        return f'your schedule for today is {table["thursday"]}'
    if weekday == 4:
        return f'your schedule for today is {table["friday"]}'
    else:
        return "you don't have any classes for today congratulations!!!"


def send_email(contents, email):
    receiver = email
    body = phrase_timetable(contents)
    yag = yagmail.SMTP('andriitccnt@gmail.com')
    yag.send(
        to=receiver,
        subject='Scheduler test mail',
        contents=body,
    )


#send_email(timetable_test)






