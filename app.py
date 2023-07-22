import streamlit as st
from preProcessor import preproces
import functionality
import SessionState
import matplotlib.pyplot as plt

# Commenting out unused import
# from cProfile import label

# Rest of the code...

i = 0
st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    # read file as bytes
    bytes_data = uploaded_file.getvalue()
    # converting uploaded data into string
    data = bytes_data.decode('utf-8')
    # st.text(data) to show data
    df = preproces(data)
    st.dataframe(df) # to show dataframe

    # fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox('Analysis for', user_list)

    Slidebtn = st.sidebar.button('Show Analysis')
    if Slidebtn or st.session_state.get('Slidebtn', False):
        st.session_state['Slidebtn'] = True

        num_msg, words, show_msg, media, links = functionality.fetch_stats(selected_user, df)
        num_overall, words_overall, show_msg_overall, media_overall, links_overall = functionality.fetch_stats('Overall', df)
        st.title(selected_user, " Analysis")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header('Total Msgs')
            st.header(num_msg)
            st.write('This is ', round((num_msg / num_overall) * 100, 3), '%', 'of Total Messages')
            msgbtn = st.button('Show Msg')
            msgbtn1 = st.button('Hide Msg')
            if selected_user != "Overall":
                if msgbtn:
                    st.write(show_msg)
                elif msgbtn1:
                    st.write('')
            else:
                st.write("Sorry, this service isn't available for Overall")
        with col2:
            st.header('Total Words')
            st.header(words)
            st.write('This is ', round((words / words_overall) * 100, 3), '%', 'of Total Words')
        with col3:
            st.header('Media')
            st.header(media)
            st.write('This is ', round((media / media_overall) * 100, 3), '%', 'of Total Media')
        with col4:
            st.header('links')
            st.header(len(links))
            st.write('This is ', round((len(links) / len(links_overall)) * 100, 3), '%', 'of Total Links')
            linkbtn = st.button('Show')
            linkbtn1 = st.button('Hide')
            if linkbtn or st.session_state.get('linkbtn', False):
                st.write(links)
            if linkbtn1:
                st.session_state['Slidebtn'] = False

        st.header('Most Common Emojis')
        col1, col2, col3 = st.columns([10, 2, 10])
        emoji_df, emo_pie_df = functionality.com_emojis(selected_user, df)
        with col1:
            st.dataframe(emoji_df)
        with col3:
            fig2, ax2 = plt.subplots()
            labels = emo_pie_df['Emojis']
            plt.title('Emojis Distribution', weight='bold', color='#333333')

            exp = []
            for i in range(len(emo_pie_df) - 1):
                exp.append(0)
            exp.append(0.1)
            exp = tuple(exp)
            ax2.pie(emo_pie_df['Occurence'], explode=exp, labels=emo_pie_df['Emojis'], autopct='%1.1f%%', shadow=True)
            ax2.axis('equal')
            st.pyplot(fig2)

        if selected_user == 'Overall':
            st.header('Most Velle Log')
            col1, col2, col3 = st.columns([5, 1, 5])
            x, busy_user_df, x2, y2 = functionality.busy_user(df)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values)
                bars = plt.bar(x.index, x.values)
                for bar in bars:
                    plt.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 30,
                        round(bar.get_height(), 1),
                        horizontalalignment='center',
                    )
                plt.title('Top 10 Vele Log', weight='bold', color='#333333')
                plt.xlabel('Name of veles', weight='500', size='14')
                plt.ylabel('No. of messages', weight='500', size='14')
                plt.xticks(rotation=50, horizontalalignment='right')
                st.pyplot(fig, width=70)

            with col3:
                fig1, ax1 = plt.subplots()
                ax1.pie(x2, labels=y2, autopct='%1.1f%%', shadow=True, startangle=90)
                plt.axis('equal')
                plt.title('Top 10 Vele Log', weight='bold', color='#333333')
                st.pyplot(fig1)
            st.header("Overall People contribution")
            st.dataframe(busy_user_df, height=450)

        st.markdown("***")
        st.header('Most Commonly Used Word')
        df_wc = functionality.word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        plt.imshow(df_wc)
        plt.axis('off')
        st.pyplot(fig)

        st.subheader('Top 25 Most Used Words')
        st.write('Deleted + message = Total deleted msg within 1 hour')
        st.write('Word filtration Applied')
        comWord_df = functionality.common_word(selected_user, df)
        st.dataframe(comWord_df)

    option = st.sidebar.selectbox('Analysis view', ('Months', 'Year', 'week'))
