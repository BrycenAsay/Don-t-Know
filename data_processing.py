"""
This file is for data analytics on previously collected twitter data for a list of users! 
(Preferably collected using my files so that none of the SQL queries, functions, code, etc. have to be updated)
***Please make sure you have all dependcies installed before trying to run any functions!***
"""
from sqlalchemy import create_engine, text
import pandas as pd
from config import USER, PASSWORD, HOST, DATABASE
import logging
import string
from collections import Counter

def months_for_specific_year(dates, years_to_go_forward, months_in_final_year):
    # a function I wrote to complie a list of every month-year from the earliest date of a tweet I retrieved to the most recent;
    # the 'dates' parameter is a list with the first item being 'year-month-day' (please note the day value only exists so you can insert it as a date type in a database)
    for i in range(years_to_go_forward):
        if dates[5:7] == 1:
            m = 1
        else:
            m = int(dates[-1][5:7])
        while m < 12:
            prev_date = dates[-1]
            if int(prev_date[5:7]) < 9:
                dates.append(f'{prev_date[0:5]}0{str(int(prev_date[5:7]) + 1)}{prev_date[7:10]}')
            else:
                dates.append(f'{prev_date[0:5]}{str(int(prev_date[5:7]) + 1)}{prev_date[7:10]}')
            m += 1
        dates.append(f'{str(int(prev_date[0:4]) + 1)}-01{prev_date[7:10]}')
    for i in range(months_in_final_year):
        prev_date = dates[-1]
        dates.append(f'{prev_date[0:5]}0{str(int(prev_date[5:7]) + 1)}{prev_date[7:10]}')
    return dates

def get_valid_dates(_username):
    # filters dates where a specified value isn't null for a date, therefore avoiding errors when inserting data into database
    engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')
    with engine.connect() as conn:
        list_o_valid_dates = []
        sql = text(f"SELECT DISTINCT DATE_FORMAT(created_on, '%Y-%m-01') AS `month-year` FROM `twitter_data for user {_username}` WHERE is_retweet=0 AND media_type='video' AND media_views IS NOT NULL")
        try:
            yes = conn.execute(sql)
            conn.commit()
            for row in yes:
                list_o_valid_dates.append(row[0])
            return list_o_valid_dates
        except:
            print("Did not work")
            conn.rollback()
        conn.close()

def get_stats_for_keyword(_users, _keyword):
    # for a list of users and a keyword, selects tweets (not including retweets) that includes the keyword then complies stats such as likes, retweets, and replies
    engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')
    usernames = {'users': _users}
    total_average_likes = 0
    total_average_retweets = 0
    total_average_replies = 0
    list_o_tweets_likes = []
    list_o_tweets_retweets = []
    list_o_tweets_replies = []
    with engine.connect() as conn:
        for username in usernames['users']:
            sql = text(f"SELECT * FROM `twitter_data for user {username}` WHERE text LIKE '%{_keyword}%' AND is_retweet=0")
            try:
                yes = conn.execute(sql)
                conn.commit()
                print(yes)
                for row in yes:
                    print(row)
                    list_o_tweets_likes.append(row[4] / row[-1])
                    list_o_tweets_retweets.append(row[6] / row[-1])
                    list_o_tweets_replies.append(row[7] / row[-1])
            except Exception as e:
                logging.error('did not work: ', e)
                conn.rollback()
        for i in range(len(list_o_tweets_likes)):
            total_average_likes += list_o_tweets_likes[i]
            total_average_retweets += list_o_tweets_retweets[i]
            total_average_replies += list_o_tweets_replies[i]
        jimmy_likes = (total_average_likes / len(list_o_tweets_likes)) * 10000
        jimmy_retweets = (total_average_retweets / len(list_o_tweets_retweets)) * 10000
        jimmy_replies = (total_average_replies / len(list_o_tweets_replies)) * 10000
        sql = text(f'INSERT INTO average_likes_per_keyword(keyword, average_likes_per_ten_thousand, average_retweets_per_ten_thousand, average_replies_per_ten_thousand) VALUES (\'{_keyword}\', {jimmy_likes}, {jimmy_retweets}, {jimmy_replies})')
        try:
            conn.execute(sql)
            conn.commit()
        except Exception as e:
            logging.error('did not work: ', e)
            conn.rollback()
        conn.close()

def get_average_likes_per_tweet_by_month(_users):
    # calculates average likes per tweets (adjusted based on amount of followers at a given point in time) filtered for a specified month
    engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')
    usernames = {'users': _users}
    list_o_year_month = []
    list_o_tweet_counts = []
    list_o_average_likes = []
    double_group_by = {}
    with engine.connect() as conn:
        for username in usernames['users']:
            sql = text(f"""SELECT CONCAT(YEAR(created_on), '-', MONTH(created_on)) AS `year-month`, 
                        COUNT(text) AS `total_tweets`, 
                        AVG(likes) AS `average likes`
                        FROM `twitter_data for user {username}`
                        WHERE is_retweet=0
                        GROUP BY `year-month`""")
            try:
                yes = conn.execute(sql)
                conn.commit()
                for row in yes:
                    list_o_year_month.append(row[0])
                    list_o_tweet_counts.append(row[1])
                    list_o_average_likes.append(row[2])
            except Exception as e:
                logging.error('did not work: ', e)
                conn.rollback()
        double_group_by['year_month'] = list_o_year_month
        double_group_by['tweet_count'] = list_o_tweet_counts
        double_group_by['average_likes'] = list_o_average_likes
        pandas_dataframe = pd.DataFrame(double_group_by)
        conn.close()
    pandas_dataframe.to_sql(f'double_group_by', engine)

def get_tweet_and_retweet_counts(_users):
    # collects the total amount of tweets and retweet counts for a group of users
    engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')
    usernames = {'users': _users}
    regular_counts = []
    retweet_counts = []
    reg_count_add = [None] * 24
    ret_count_add = [None] * 24
    likes_and_retweets = {}
    with engine.connect() as conn:
        for username in usernames['users']:
            regular_count_sql = text(f"""SELECT COUNT(text) AS `total_retweets`
                        FROM `twitter_data for user {username}`
                        WHERE is_retweet=0;""")
            retweet_count_sql = text(f"""SELECT COUNT(text) AS `total_retweets`
                        FROM `twitter_data for user {username}`
                        WHERE is_retweet=1;""")
            try:
                reg_count = conn.execute(regular_count_sql)
                twt_count = conn.execute(retweet_count_sql)
                conn.commit()
                for row in reg_count:
                    regular_counts.append(row[0])
                for row in twt_count:
                    retweet_counts.append(row[0])
            except Exception as e:
                logging.error('did not work: ', e)
                conn.rollback()
        _usernames = (usernames['users'] + usernames['users'])
        likes_and_retweets['usernames'] = _usernames
        regular_counts += reg_count_add
        likes_and_retweets['regular_tweet_count'] = regular_counts
        ret_count_add += retweet_counts
        likes_and_retweets['retweet_count'] = ret_count_add
        pandas_dataframe = pd.DataFrame(likes_and_retweets)
        conn.close()
    pandas_dataframe.to_sql(f'reg&retc_per_user', engine)

def get_avg_likes_for_replies_and_regular_tweets(_users):
    # retrieves the averages likes for regular tweets and the average amount of likes for replies (it filters replies based on wether the tweet starts with '@')
    engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')
    usernames = {'users': _users}
    regular_counts = []
    reply_counts = []
    raw_total_reply_count = []
    total_tweet_count = []
    total_reply_count = []
    likes_and_retweets = {}
    with engine.connect() as conn:
        for username in usernames['users']:
            avg_like_reply_sql = text(f"""SELECT AVG(likes) AS avg_likes FROM `twitter_data for user {username}`
                                        WHERE text like '@%';""")
            avg_like_reg_sql = text(f"""SELECT AVG(likes) AS avg_likes FROM `twitter_data for user {username}`
                                        WHERE text not like '@%';""")
            total_reply_count_sql = text(f"""SELECT COUNT(`text`)
                                            FROM `twitter_data for user {username}`
                                            WHERE `text` LIKE '@%'""")
            total_tweet_count_sql = text(f"""SELECT COUNT(`text`)
                                            FROM `twitter_data for user {username}`""")
            try:
                rep_count = conn.execute(avg_like_reply_sql)
                reg_count = conn.execute(avg_like_reg_sql)
                raw_tot_rep_count = conn.execute(total_reply_count_sql)
                tot_twt_count = conn.execute(total_tweet_count_sql)
                conn.commit()
                for row in rep_count:
                    reply_counts.append(row[0])
                for row in reg_count:
                    regular_counts.append(row[0])
                for row in raw_tot_rep_count:
                    raw_total_reply_count.append(row[0])
                for row in tot_twt_count:
                    total_tweet_count.append(row[0])
            except Exception as e:
                logging.error('did not work: ', e)
                conn.rollback()
        for i in range(len(raw_total_reply_count)):
            total_reply_count.append((raw_total_reply_count[i] / total_tweet_count[i]) * 3000)
        _usernames = usernames['users']
        likes_and_retweets['usernames'] = _usernames
        likes_and_retweets['regular_avg_likes'] = regular_counts
        likes_and_retweets['reply_avg_likes'] = reply_counts
        likes_and_retweets['total_reply_count'] = total_reply_count
        pandas_dataframe = pd.DataFrame(likes_and_retweets)
        conn.close()
    pandas_dataframe.to_sql(f'avg_like_for_rep&reg', engine)

def most_frequent_word_above_six_chars(_users):
    # gets the most frequent six letter word appearing through all of the retrieved tweets for a given user
    def highest_five_letter_word(text):
        # Remove all punctuation from the text
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Split the text into a list of words
        words = text.split()
        # Count the occurrences of each six-letter word in the list
        counts = Counter(word for word in words if len(word) == 6)
        # Return the most common six-letter word
        return counts.most_common(1)[0] if counts else None

    engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')
    usernames = {'users': _users}
    data_dict = {}
    most_common_word_above_five_letters = []
    mcwafl_count = []
    with engine.connect() as conn:
        for username in usernames['users']:
            all_text_sql = text(f"""SELECT `text` FROM `twitter_data for user {username}`
                                        WHERE is_retweet=0;""")
            try:
                big_messy_str = ""
                all_text = conn.execute(all_text_sql)
                conn.commit()
                for row in all_text:
                    big_messy_str += f' {row[0]}'
                yea = highest_five_letter_word(big_messy_str)
                yea_word = yea[0]
                yea_count = yea[1]
                most_common_word_above_five_letters.append(yea_word)
                mcwafl_count.append(yea_count)
            except Exception as e:
                logging.error('did not work: ', e)
                conn.rollback()
        conn.close()
    data_dict['username'] = usernames['users']
    data_dict['most_common_word'] = most_common_word_above_five_letters
    data_dict['count'] = mcwafl_count
    pandas_dataframe = pd.DataFrame(data_dict)
    pandas_dataframe.to_sql(f'most_common_six_letter_word', engine)

def average_retweets_for_retweets(_users):
    # calculates how many retweets the tweets that a user's retweets has... confusing wording but hopefully that makes sense XD
    engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')
    usernames = {'users': _users}
    avg_retweets_for_retweets = []
    data_dict = {}
    with engine.connect() as conn:
        for username in usernames['users']:
            avg_ret_for_ret_sql = text(f"""SELECT AVG(retweets)
                                            FROM `twitter_data for user {username}`
                                            WHERE is_retweet=1;""")
            try:
                avg_ret_for_ret = conn.execute(avg_ret_for_ret_sql)
                conn.commit()
                for row in avg_ret_for_ret:
                    avg_retweets_for_retweets.append(row[0])
            except Exception as e:
                logging.error('did not work: ', e)
                conn.rollback()
        _usernames = usernames['users']
        data_dict['usernames'] = _usernames
        data_dict['average_retweets_for_retweets'] = avg_retweets_for_retweets
        data_dict['popularity_class'] = ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C', 'D', 'D', 'D', 'F', 'F', 'F', 'X', 'X', 'X', 'Y', 'Y', 'Y', 'Z', 'Z', 'Z']
        pandas_dataframe = pd.DataFrame(data_dict)
        conn.close()
    pandas_dataframe.to_sql(f'retweets_avg_retweets', engine)

def total_animated_gifs(_users):
    # returns the total animated gifs for a list of specified users
    engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}')
    usernames = {'users': _users}
    gif_counts = []
    data_dict = {}
    with engine.connect() as conn:
        for username in usernames['users']:
            count_gifs_sql = text(f"""SELECT COUNT(*)
                                            FROM `twitter_data for user {username}`
                                            WHERE media_type='animated_gif' AND is_retweet=0;""")
            try:
                gif_count = conn.execute(count_gifs_sql)
                conn.commit()
                for row in gif_count:
                    gif_counts.append(row[0])
            except Exception as e:
                logging.error('did not work: ', e)
                conn.rollback()
        _usernames = usernames['users']
        data_dict['usernames'] = _usernames
        data_dict['total_gifs'] = gif_counts
        pandas_dataframe = pd.DataFrame(data_dict)
        conn.close()
    pandas_dataframe.to_sql(f'gif_counts', engine)

def main():
    # these are the users I used; put whatever list of users you want though! (Make sure they are actually present in your database or it will throw an error!)
    users = ['justinbieber', 'rihanna', 'katyperry', 'BrunoMars', 'NiallOfficial', 'MileyCyrus', 'SnoopDogg', 'coldplay',
                                    'ricky_martin', 'sza', 'Metallica', 'paramore', 'blink182', 'foofighters', 'ChloeBailey', 'boniver', 'Hozier',
                                    'tameimpala', 'TDCinemaClub', 'thelumineers', 'CAVETOWN', 'headandtheheart', 'ShakeyGraves', 'sleepingatlast']
    # put whatever data analytics functions you want to run here! They should automatically update into your databases for further querying/data visualization :)
    pass

if __name__ == '__main__':
    main()