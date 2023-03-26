import streamlit as st
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import helper

st.sidebar.title('Whatsapp Chat Analyser 2.0')

uploaded_file = st.sidebar.file_uploader('Upload the whatsapp text file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = helper.preprocess(data)

    user_list = [x for x in df.USERNAME.unique() if x != 'Notification']
    user_list.insert(0, 'Overall')
    username = st.sidebar.selectbox('Show Analysis for: ', user_list)

if st.sidebar.button('Show Analysis'):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.header('Total Messages')
        st.title(helper.total_messages_count(df, username))

    with col2:
        st.header('Total Words')
        st.title(helper.total_word_count(df, username))

    with col3:
        st.header('Media Shared')
        st.title(helper.media_shared(df, username))

    with col4:
        st.header('Links Shared')
        st.title(helper.links_shared(df, username))

    if username == 'Overall':
        col1, col2 = st.columns(2)

        with col1:
            st.title('Top 10 most active members')
            st.dataframe(helper.most_active_members(df))

        with col2:
            st.title('Top 10 least active members')
            st.dataframe(helper.least_active_members(df))

    st.title('Emoji Analysis')
    st.dataframe(helper.emoji_count(df, username), width=750)

    st.title('WordCloud - Frequency of Words')
    wc = helper.wordcloud_generator(df, username)
    plt.figure(figsize=(8, 8), facecolor=None)
    fig, ax = plt.subplots()
    ax.imshow(wc)
    st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        st.title("Daily Message Surge")
        day_wise_df = helper.day_wise_plot(df, username)
        fig, ax = plt.subplots()
        ax.bar(day_wise_df.index, day_wise_df.MESSAGE.values)
        st.pyplot(fig)

    with col2:
        st.title("Monthly Message Surge")
        month_wise_df = helper.month_wise_plot(df, username)
        fig, ax = plt.subplots()
        ax.bar(month_wise_df.index, month_wise_df.MESSAGE.values)
        st.pyplot(fig)





