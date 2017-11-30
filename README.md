

This project is mostly an example of combining many different technologies into one script.

The modules it uses are as follows

 - requests
 - boto3 
 - praw
 - uuid
 - I/O with txt files
 
 The script does the following.
 
 First requests https://newsapi.org and grabs all the articles ordered by 'Top'.
 
 Next it saves it to a text file. Unless the script has been run already and a txt file exists.
 
 In that case, it reads the existing text file and saves any new articles to the file.
 
 Then it prunes the txt file for articles that were no longer returned from the requests.
 
 In essence the articles that exist in the text file, but not in the returned requests are no longer in the news.
 
 So it then posts that article to reddit in the /r/thenewsrightnow subreddit.
 
 The last thing it does is stores the article including title, author, and other features to a DynamoDB on AWS.
 
 
 Skills learned are requesting data from an api, saving and reading text/csv, dictionary manipulation, DynamoDB, Praw (reddit module)
 AWS ssh scp and crontab, patience.
