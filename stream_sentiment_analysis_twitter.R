#install.packages("streamR")
#install.packages("RSentiment")

library(ROAuth)
library("streamR")

library(RCurl)
library(stringr)
library("plyr")
library(RSentiment)
#Please add new key words if you have more . use , to separate
key_list="@UPS,#ups,@ups,#UPS"

# use | to separete different keywords you want to filter out
remove_key ="@yyy"
loop_time = 10


    # requestURL <- "https://api.twitter.com/oauth/request_token"
    # accessURL <- "https://api.twitter.com/oauth/access_token"
    # authURL <- "https://api.twitter.com/oauth/authorize"
    # consumerKey <- "xxxxxx"
    # consumerSecret <- "xxxxxxxxxx"
    # my_oauth <- OAuthFactory$new(consumerKey = consumerKey, consumerSecret = consumerSecret, 
    #                              requestURL = requestURL, accessURL = accessURL, authURL = authURL)
    # my_oauth$handshake(cainfo = system.file("CurlSSL", "cacert.pem", package = "RCurl"))
    #save(my_oauth, file = "my_oauth.Rdata")

load("my_oauth.Rdata")
pos= scan('positive-words.txt',what='character',comment.char = ';')
neg= scan('negative-words.txt',what='character',comment.char = ';')
source('sentiment_new_v2.r')


tweets <- filterStream( file.name="", track=key_list, timeout=loop_time,language="en", oauth=my_oauth )
tweets_df <- parseTweets(tweets, verbose = FALSE)
tweets_df <- tweets_df[(tweets_df$user_lang=="en" & (tweets_df$country_code=="US" | is.na(tweets_df$country_code))),]
tweets_df <- tweets_df[ ! grepl(remove_key,tweets_df$text),]

  if (nrow(tweets_df)>0)   {
    #score.sentiment in another file sourced earlier
    #kept separate so that we can change scoring scheme if needed 
    analysis_result=score.sentiment(tweets_df$text,pos,neg)
    sentiment_score<- analysis_result$score
    tweets_df <- cbind(tweets_df,sentiment_score) 
    df_neg <- tweets_df[tweets_df$sentiment_score<0 ,]  
    df_neg
      }   else   
        {
        print(paste("no tweets ", tag))
  }
