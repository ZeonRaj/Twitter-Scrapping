
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import streamlit as st
import datetime
import json

from pymongo import MongoClient


# check the emojis in this link https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Twitter Scraping", page_icon=":octopus:",layout='wide')

#------Header section____

st.title("Twitter Scraping")
st.subheader("hi,I am Zeon")
st.write("this is a basic project for my github portfolio")
#st.write("type thw Hasttag")
Hashtag = st.text_input ("input Hashtag")
# to input start and end date
col1,col2=st.columns(2)
with col1:
    Start_date=st.date_input(
        "From",
        datetime.date(2023,1,10))
    st.write('From:',"Start_date")
with col2:
    stop_date =st.date_input(
        "End",
        datetime.date(2023,2,1))
    st.write('End:',stop_date)

# to input data as string
start_date_s=str(Start_date)
stop_date_s=str(stop_date)

Twit_Limit = st.number_input('No. Of Tweets', min_value=1, max_value=1000)
# create a search button
search=st.button("go")
#to download the data
Data_DB=st.button("download")
# to create a list to append tweet data
tweets_list2=[]
#using TwitterSearchScraper to scrape data and append tweets
if search or Data_DB:
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(Hashtag+' since:'+start_date_s+
                                                            ' until:'+stop_date_s).get_items()):
        if i>Twit_Limit:
             break
        tweets_list2.append([tweet.date, tweet.id, tweet.content, tweet.user.username,
                             tweet.replyCount, tweet.retweetCount,
                             tweet.lang, tweet.source, tweet.likeCount])
    tweets_df2 =pd.DataFrame(tweets_list2,
                             columns=['Datetime','Tweet Id','Text', 'Username', 'ReplyCount', 'RetweetCount',
                                   'Language', 'Source', 'LikeCount'])
    st.dataframe(tweets_df2)

client = MongoClient(("mongodb://localhost:27017"))
                      
db =client["Twitter_Data"]

if Data_DB:
    Chennai_Topic_1=db[Hashtag]

    tweets_df2.reset_index(inplace=True)
    tweets_df2_dict = tweets_df2.to_dict("records")
    Chennai_Topic_1.insert_one({"index": Hashtag + 'data', "data": tweets_df2_dict})


    data_from_db = Chennai_Topic_1.find_one({"index":Hashtag+'data'})
    df = pd.DataFrame(data_from_db["data"])
    df.to_csv("Twitter_data.csv")
    df.to_json("Twitter_data.json")

    st.download_button("Download CSV",
                   df.to_csv(),
                   mime = 'text/csv')

    st.download_button("Download Json",
                       df.to_json(),
                       mime='json')



                
            



