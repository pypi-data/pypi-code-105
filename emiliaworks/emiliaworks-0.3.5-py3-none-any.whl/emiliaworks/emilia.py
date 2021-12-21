class custom:    

    def __init__(self,searchstring,searchstrsince,searchstruntil):
        self.searchstring = searchstring
        self.searchstrsince = searchstrsince
        self.searchstruntil = searchstruntil

    def get_tweets(self):
        import twint
        import nest_asyncio
        c = twint.Config()
        c.Limit = 10
        c.Lang = 'en'
        c.Pandas = True
        c.Search = self.searchstring
        c.Replies = True
        c.Since = self.searchstrsince
        c.Until = self.searchstruntil
        c.Popular_tweets = True
        c.Pandas_clean = True
        c.Min_replies = 1
        nest_asyncio.apply()
        twint.run.Search(c)
        self.Tweets_df = twint.storage.panda.Tweets_df
        return(self.Tweets_df)

    def clean_data(self):
        df = self.Tweets_df
        import pandas as pd
        from bs4 import BeautifulSoup
        from nltk.tokenize import RegexpTokenizer
        import emoji
        import re
        tokenizer = RegexpTokenizer('\w+|$[\d\.]+|http\S+http\S+|www.\S+co')
        count=0
        listt = []
        for tw in df['tweet']:
            count = count+1
            tweetlist1 = tw
            tweetlist = tweetlist1.split()
            string_uncleaned = ' '.join(tweetlist)
            string_uncleaned = BeautifulSoup(string_uncleaned).get_text()
            string_emojiless = emoji.get_emoji_regexp().sub(u'',string_uncleaned)
            string_emojiless = re.sub(r"http\S+", "", string_emojiless)
            string_emojiless = re.sub(r"@\S+", "", string_emojiless)
            cleaned_output1 = string_emojiless
            listt.append(cleaned_output1)
        df['clean']=listt
        self.clean_df = df
        return(self.clean_df)

    def siamod(self):
        import matplotlib
        df = self.clean_df
        from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
        sia = SIA()
        df['Sentiment_Compound'] = df.clean.apply(lambda x: sia.polarity_scores(x)['compound'])
        df['Sentiment_Positive'] = df.clean.apply(lambda x: sia.polarity_scores(x)['pos'])
        df['Sentiment_Negative'] = df.clean.apply(lambda x: sia.polarity_scores(x)['neg'])
        df['Sentiment_Neutral'] = df.clean.apply(lambda x: sia.polarity_scores(x)['neu'])
        df['sphere_of_influence1'] = ((self.clean_df['nreplies']+df['nlikes']+df['nretweets'])/3)*df['Sentiment_Compound']
        result_df = df.groupby(['date']).mean()
        return(result_df)

    #emiliaindex = emilia.inputs()
    #emiliaindex.get_tweets()
    #emiliaindex.clean_data()
    #emiliaindex.siamod()