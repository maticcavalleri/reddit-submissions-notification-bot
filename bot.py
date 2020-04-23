import praw
import re

class RedditBot():
    def __init__(self, cred_file='cred.txt'):
        """ authenticates itself upon creation """
        self.cred_dict = self.get_credentials_from_file(cred_file)
        self.reddit = praw.Reddit(client_id=self.cred_dict['client_id'],
                        client_secret=self.cred_dict['client_secret'], password=self.cred_dict['password'],
                        user_agent=self.cred_dict['user_agent'], username=self.cred_dict['username'])
        self.user_list = []

    def main(self):
        """ where things go down """
        subreddit = self.reddit.subreddit('PhotoshopRequest')

        # pause_after -1 required so two streams can run simultaneously
        inbox_stream = self.reddit.inbox.stream(pause_after=-1)
        submission_stream = subreddit.stream.submissions(pause_after=-1)

        # while True wouldn't be required if there was only one stream
        while True:
            self.run_stream(inbox_stream, self.inbox_handler)
            self.run_stream(submission_stream, self.submission_handler)

    def run_stream(self, stream, handler):
        """ loops through the given stream and calls the given handler to handle the fetched data """
        for item in stream:
            if item is None:
                break
            handler(item)

    def inbox_handler(self, message):
        """ handles new personal messages """
        if "unsubscribe" in message.body.lower():
            self.user_list.remove(str(message.author))
            self.reddit.redditor(str(message.author)).message(
                'successfully unsubscribed',
                'You have been successfully **unsubscribed** from receiving messages from this bot.\n\n\n'
                '*^I\'m ^a ^bot, ^bleep, ^bloop*'
                )
            print('unsubbed')
            
        elif "subscribe" in message.body.lower() and str(message.author) not in self.user_list:
            self.user_list.append(str(message.author))
            self.reddit.redditor(str(message.author)).message(
                'successfully subscribed',
                'You have been successfully **subscribed** from receiving messages from this bot.\n\n\n'
                '*^I\'m ^a ^bot, ^bleep, ^bloop*'
                )
            print('subbed')
        else:
            print(message.author, message.body)
        

    def submission_handler(self, submission):
        """ handles new posts """
        # TODO handle messages
        print(submission.title)

    def get_credentials_from_file(self, file):
        """ gets all credentials required for authentication """
        cred_dict = {}
        file = open(file, "r")
        for line in file.readlines():
            temp = line.replace('\t', '').replace(' ', '').strip().split('=')
            cred_dict[str(temp[0])] = str(temp[1])
        return cred_dict

if __name__ == "__main__":
    bot = RedditBot()
    bot.main()
