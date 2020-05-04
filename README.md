# reddit-submissions-notification-bot
A bot that sends personal message whenever a specific submission is posted in a subreddit. Bot is written with Python using PRAW (Python Reddit API Wrapper). Bot is meant to be used by multiple users with it's subscription system. Perfect for use in subreddits that would like to have an ability to notify it's users that are subscribed to the bot when submission with particualr traits gets posted.

### CURRENT CONFIGURATION:
Currently configured to send a personal message on reddit to all of it's subscribers whenever a submission with "paid" flair is posted in a subreddit "r/PhotoshopRequest".

### HOW TO SET UP:
1. Create a Reddit bot account
2. Rename "\_cred.txt" to "cred.txt" and inside of it enter your bot's credentials. If this step is skipped you will be prompted to enter credentials via terminal
3. Modify the code to your likings (change subreddit, method of triggering message...)
4. You are all set up. You can now start running the script :)

### HOW TO SUBSCRIBE:
In order to subscribe to the bot you have to send a personal message to the bot containing keyword "subscribe" in message body. In order to unsubscribe the keyword is "unsubscribe".
