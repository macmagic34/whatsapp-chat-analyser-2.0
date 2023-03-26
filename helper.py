import re
import numpy as np
import pandas as pd
import wordcloud
from urlextract import URLExtract
from collections import defaultdict


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s[a-z]{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    date_time = re.findall(pattern, data)
    date_time = [x.replace('\u202f', ' ') for x in date_time]
    df = pd.DataFrame({'USER_MESSAGES': messages, 'DATE_TIME': date_time})
    df['DATE_TIME'] = pd.to_datetime(df['DATE_TIME'], format='%d/%m/%y, %I:%M %p - ')
    df['YEAR'] = df.DATE_TIME.dt.year
    df['MONTH'] = df.DATE_TIME.dt.month_name()
    df['DAY'] = df.DATE_TIME.dt.day
    df["DAY_NAME"] = df.DATE_TIME.dt.day_name()
    df['HOUR'] = df.DATE_TIME.dt.hour
    df['MINUTE'] = df.DATE_TIME.dt.minute
    df[['USERNAME', 'MESSAGE']] = df[df.USER_MESSAGES.str.contains(':')].USER_MESSAGES.str.split(':', 1, expand=True)
    df['USERNAME'] = np.where(~df.USER_MESSAGES.str.contains(':'), 'Notification', df['USERNAME'])
    df['MESSAGE'] = np.where(~df.USER_MESSAGES.str.contains(':'), df.USER_MESSAGES, df['MESSAGE'])
    return df


def total_messages_count(dataframe, username='Overall'):
    if username is 'Overall':
        return dataframe.shape[0]
    else:
        return dataframe[dataframe.USERNAME == username].shape[0]


def total_word_count(dataframe, username='Overall'):
    if username is 'Overall':
        return dataframe.MESSAGE.str.split().str.len().sum()
    else:
        return dataframe[dataframe.USERNAME == username].MESSAGE.str.split().str.len().sum()


def media_shared(dataframe, username='Overall'):
    if username is 'Overall':
        return dataframe[dataframe.MESSAGE == ' <Media omitted>\n'].shape[0]
    else:
        return dataframe[(dataframe.MESSAGE == ' <Media omitted>\n') & (dataframe.USERNAME == username)].shape[0]


def links_shared(dataframe, username='Overall'):
    extractor = URLExtract()
    if username is 'Overall':
        combined_string = ' '.join(dataframe.MESSAGE)
        urls = extractor.find_urls(combined_string)
        return len(urls)
    else:
        combined_string = ' '.join(dataframe[dataframe.USERNAME == username].MESSAGE)
        urls = extractor.find_urls(combined_string)
        return len(urls)


def emoji_count(dataframe, username='Overall'):
    emoji_count = defaultdict(int)
    if username is 'Overall':
        for i in dataframe['MESSAGE']:
            for emoji in re.findall(u'[\U0001f300-\U0001f650]|[\u2000-\u3000]', i):
                emoji_count[emoji] += 1
        return dict(sorted(emoji_count.items(), key=lambda x: x[1], reverse=True)[:20])
    else:
        for i in dataframe[dataframe.USERNAME == username]['MESSAGE']:
            for emoji in re.findall(u'[\U0001f300-\U0001f650]|[\u2000-\u3000]', i):
                emoji_count[emoji] += 1
        return dict(sorted(emoji_count.items(), key=lambda x: x[1], reverse=True)[:20])


def most_active_members(dataframe):
    return pd.DataFrame(
        {"No. of Messages": dataframe.USERNAME.value_counts().sort_values(ascending=False).nlargest(10)})


def least_active_members(dataframe):
    return pd.DataFrame(
        {"No. of Messages": dataframe.USERNAME.value_counts().sort_values(ascending=False).nsmallest(10)})


def wordcloud_generator(dataframe, username='Overall'):
    if username == 'Overall':
        str_messages = ''
        str_messages += " ".join(dataframe.MESSAGE) + " "
        str_messages_lower_case = str_messages.lower()
        wc = wordcloud.WordCloud(width=800, height=800,
                                 background_color='white',
                                 stopwords=wordcloud.STOPWORDS,
                                 min_font_size=10).generate(str_messages_lower_case)
        return wc
    else:
        str_messages = ''
        str_messages += " ".join(dataframe[dataframe.USERNAME == username].MESSAGE) + " "
        str_messages_lower_case = str_messages.lower()
        wc = wordcloud.WordCloud(width=800, height=800,
                                 background_color='white',
                                 stopwords=wordcloud.STOPWORDS,
                                 min_font_size=10).generate(str_messages_lower_case)
        return wc


def day_wise_plot(dataframe, username='Overall'):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    if username == 'Overall':
        day_wise_counts = dataframe.groupby(['DAY_NAME'])['MESSAGE'].count()
        day_wise_counts = day_wise_counts.reset_index()
        day_wise_counts['DAY_NAME'] = day_wise_counts['DAY_NAME'].apply(lambda x: x[:3])
        # day_wise_counts.drop(['level_0', 'index'], axis=1, inplace=True)
        day_wise_counts.set_index('DAY_NAME', inplace=True)
        day_wise_counts.reindex(days)
        return day_wise_counts
    else:
        day_wise_counts = dataframe[dataframe.USERNAME == username].groupby(['DAY_NAME'])['MESSAGE'].count()
        day_wise_counts = day_wise_counts.reset_index()
        day_wise_counts['DAY_NAME'] = day_wise_counts['DAY_NAME'].apply(lambda x: x[:3])
        # day_wise_counts.drop(['level_0', 'index'], axis=1, inplace=True)
        day_wise_counts.set_index('DAY_NAME', inplace=True)
        day_wise_counts.reindex(days)
        return day_wise_counts


def month_wise_plot(dataframe, username='Overall'):
    months = ['Jan', 'Feb', "Mar", 'Dec']
    if username == 'Overall':
        month_wise_counts = dataframe.groupby(['MONTH'])['MESSAGE'].count()
        month_wise_counts = month_wise_counts.reset_index()
        month_wise_counts['MONTH'] = month_wise_counts['MONTH'].apply(lambda x: x[:3])
        # month_wise_counts.drop(['level_0', 'index'], axis=1, inplace=True)
        month_wise_counts.set_index('MONTH', inplace=True)
        month_wise_counts.reindex(months)
        return month_wise_counts
    else:
        month_wise_counts = dataframe[dataframe.USERNAME == username].groupby(['MONTH'])['MESSAGE'].count()
        month_wise_counts = month_wise_counts.reset_index()
        month_wise_counts['MONTH'] = month_wise_counts['MONTH'].apply(lambda x: x[:3])
        # month_wise_counts.drop(['level_0', 'index'], axis=1, inplace=True)
        month_wise_counts.set_index('MONTH', inplace=True)
        month_wise_counts.reindex(months)
        return month_wise_counts
