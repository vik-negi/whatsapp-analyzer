import pandas as pd
import numpy as np
import re

def preproces(data):
    # from typing import Pattern
    AmPm = False
    # Pattern For 12hours timing
    # pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:am|pm)\s-\s'
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:] #we use this to avoid first '' in youe msg
    # Pattern For 24 hours timing
    if messages == []:
        AmPm = True
        # pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
        pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:am|pm)\s-\s'
        messages = re.split(pattern, data)[1:] #we use this to avoid first '' in youe msg

    if messages == []:
        AmPm = True
        pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:AM|PM)\s-\s'
        messages = re.split(pattern, data)[1:] #we use this to avoid first '' in youe msg

    dates = re.findall(pattern, data)
    print(len(messages), len(dates))
    df = pd.DataFrame({'user_message': messages, 'msg_date':dates})
    # df['msg_date'] = pd.to_datetime(df['msg_date'], format='%d/%m/%Y, %H:%M - ')
    # converting msg date type
    if AmPm == False:
        try:
            df['msg_date'] = pd.to_datetime(df['msg_date'], format='%d/%m/%Y, %H:%M - ')
        except:
            df['msg_date'] = pd.to_datetime(df['msg_date'], format='%m/%d/%Y, %H:%M - ')
        finally:
            df['msg_date'] = pd.to_datetime(df['msg_date'], format='%m/%d/%y, %H:%M - ')

    else:
        try:
            df['msg_date'] = pd.to_datetime(df['msg_date'], format='%m/%d/%y, %I:%M %p - ')
        except:
            df['msg_date'] = pd.to_datetime(df['msg_date'], format='%m/%d/%Y, %I:%M %p - ')
        finally:
            df['msg_date'] = pd.to_datetime(df['msg_date'], format='%d/%m/%Y, %I:%M %p - ')

        
    df.rename(columns={'dates': 'date'}, inplace=True)
    
    # seperating user and messages
    users=[]
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\w]+?):\s', message)
        if entry[1:]: #user name
            users.append(entry[0]+entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['hour'] = df['msg_date'].dt.hour
    df['minute'] = df['msg_date'].dt.minute
    df['date'] = df['msg_date'].dt.day
    df['month'] = df['msg_date'].dt.month_name()
    df['year'] = df['msg_date'].dt.year
    
    return df
    