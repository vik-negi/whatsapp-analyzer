import pandas as pd
import emoji
import sys

from wordcloud import WordCloud, STOPWORDS
from collections import Counter



def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
        # no of msg
    num_msg =  df.shape[0]
        # no of words
    words = []
    show_msg = []
    media = 0
    links = []
    for word in df['message']:
        words.extend(word.split())
        show_msg.append(word[0:-1])
        if '<Media omitted>' in word:
            media+=1
        if ('http'or'www.' or'.com'or'//') in word:
            links.append(word)
    return num_msg, len(words), show_msg, media, links

def com_emojis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    emojis = []
    for msg in df['message']:
        emojis.extend([i for i in msg if i in emoji.UNICODE_EMOJI['en']])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=('Emojis', 'Occurence'))
    sum=0
    for i in emoji_df['Occurence']:
        sum+=i
    emo_per = round(((emoji_df['Occurence']/sum)*100),3)
    emoji_df['Percentage'] = emo_per

    emo_thresold = int(0.02*sum)
    emo_pie_df = emoji_df[emoji_df['Occurence'] >=emo_thresold]
    other = 0
    for i in emoji_df['Occurence']:
        if i <emo_thresold:
            other = other + i
    other_dict = {"Emojis":'Others', 'Occurence': other,'Percentage' :(other/sum)*100}
    emo_pie_df = emo_pie_df.append(other_dict, ignore_index=True)
    emoji_df.index = emoji_df.index+1
    emo_pie_df.index = emo_pie_df.index+1
    return emoji_df, emo_pie_df


def busy_user(df):
    busy_user_df = round((df['user'].value_counts()/df.shape[0])*100, 3).reset_index().rename(columns={'index':'Name', 'user':'Percentage'})
    busy_user_df.index = busy_user_df.index+1
    x = df['user'].value_counts().head(10)
    # for pie chart
    df2 = df
    tlt_msg = df2['user'].value_counts()
    df3 = dict(tlt_msg)
    thresold = round(tlt_msg.sum()/43.6,0)
    other=0
    disk1 = {k:v for (k,v) in df3.items() if v > thresold}
    disk2 = {k:v for (k,v) in df3.items() if v < thresold}
    for i in disk2.values():
        other+=i
    disk1['others'] = other
    # disk1
    pielst = list(disk1.items())
    piedf = pd.DataFrame(pielst)
    piedf
    x1 = piedf.iloc[:,-1:].values.tolist()
    y1 = piedf.iloc[:,0:1].values.tolist()
    y2 =[]
    for i in y1:
        y2.append(i[0])
    x2 = []
    for i in x1:
        x2.append(i[0])
    return x,busy_user_df,x2,y2


def word_cloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    df2 = df
    df2.drop(df2[df2['message']=='<Media omitted>\n'].index, inplace=True)
    
    wc = WordCloud(width=1550, height=540,min_font_size = 10, background_color = 'white')
    df_wc = wc.generate(df2['message'].str.cat(sep=" "))
    return df_wc

def common_word(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    # needed to remove group notification and stop words
    temp = df[df['message']!='group_notification']
    temp = df[df['message']!='<Media omitted>\n']
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    wordss = []
    word_list=[]
    for message in temp['message']:
        for word in message.lower().split(' '):
            if '\n' in word:
                for i in word.split('\n'):
                    word_list.append(i)
            else:
                word_list.append(word)
    for word in word_list:
        if word not in stop_words and len(word)>3 and '@' not in word:
            wordss.append(word)

    comWord_df = pd.DataFrame(Counter(wordss).most_common(25), columns=('Words', 'Occurence'))
    comWord_df.index = comWord_df.index + 1
    return comWord_df
    
