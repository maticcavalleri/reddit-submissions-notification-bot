from getpass import getpass
import os.path
import shelve
import praw
import re


class RedditBot():
    def __init__(self, cred_file='cred.txt'):
        """ authenticates itself upon creation """
        self.reddit = self.authenticate(cred_file)
        # get data from database file or create one if it does not yet exist
        self.db = shelve.open('database')
        # initialize keys if they do not yet exist
        if 'processed_messages' not in self.db:
            self.db['processed_messages'] = []
        if 'processed_submissions' not in self.db:
            self.db['processed_submissions'] = []
        if 'subscribers' not in self.db:
            self.db['subscribers'] = []

    def main(self):
        """ main function that runs the program """
        subreddit = self.reddit.subreddit('PhotoshopRequest')

        # pause_after=-1 required so two streams can run simultaneously
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

    def store_data(self, key, obj):
        """ stores data locally with shelve module """
        # TODO: store only last 100 ids for submissions (and inbox?)
        temp = self.db[key]
        temp.append(obj)
        self.db[key] = temp

    def remove_data(self, key, obj):
        """ removes value from locally stored list """
        temp = self.db[key]
        temp.remove(obj)
        self.db[key] = temp

    def inbox_handler(self, message):
        """ handles new personal messages """
        if message.id in self.db['processed_messages']:
            return
        self.store_data('processed_messages', message.id)

        if "unsubscribe" in message.body.lower() and str(message.author) in self.db['subscribers']:
            self.remove_data('subscribers', str(message.author))
            self.reddit.redditor(str(message.author)).message(
                'successfully unsubscribed',
                'You have been successfully **unsubscribed** from receiving messages from this bot.\n\n\n'
                '*^I ^am ^a ^bot, ^bleep, ^bloop*'
            )

        elif "unsubscribe" in message.body.lower() and str(message.author) not in self.db['subscribers']:
            self.reddit.redditor(str(message.author)).message(
                'Already unsubscribed',
                'You are trying to **unsubscribe** but it seems like **you are not on subscription list**.\n\n\n'
                '*^I ^am ^a ^bot, ^bleep, ^bloop*'
            )

        elif "subscribe" in message.body.lower() and str(message.author) in self.db['subscribers']:
            self.reddit.redditor(str(message.author)).message(
                'Already subscribed',
                'You are trying to **subscribe** but it seems like **you are already on subscription list**.\n\n\n'
                '*^I ^am ^a ^bot, ^bleep, ^bloop*'
            )

        elif "subscribe" in message.body.lower() and str(message.author) not in self.db['subscribers']:
            self.store_data('subscribers', str(message.author))
            self.reddit.redditor(str(message.author)).message(
                'successfully subscribed',
                'You have been successfully **subscribed** to receiving messages from this bot.\n\n\n'
                '*^I ^am ^a ^bot, ^bleep, ^bloop*'
            )

        else:
            self.reddit.redditor(str(message.author)).message(
                'No command found',
                'I could not find a supported command in your message.\n'
                'currently supported commands are:\n\n**subscribe**\n**unsubscribe**\n\n'
                'These commands have to be in the body of the message.\n\n\n'
                '*^I ^am ^a ^bot, ^bleep, ^bloop*'
            )

    def submission_handler(self, submission):
        """ handles new posts """
        if submission.id in self.db['processed_submissions']:
            return
        self.store_data('processed_submissions', submission.id)
        # if no trigger word in submission flair do not notify
        if 'paid' not in submission.link_flair_text.lower():
            return
        self.notify(submission)

    def authenticate(self, file_name):
        """ gets credentials from file or from user input if no file is found """
        # get credentials from file if such file exists
        if os.path.exists(file_name):
            cred_dict = self.get_credentials_from_file(file_name)
        # if such file does not exist get credentials from user input
        else:
            print('No cred.txt file was found. Enter your credentials here:')
            cred_dict = self.get_credentials_from_input()
        try:
            reddit = praw.Reddit(username=cred_dict['username'],
                                 password=cred_dict['password'],
                                 client_id=cred_dict['client_id'],
                                 client_secret=cred_dict['client_secret'],
                                 user_agent=cred_dict['user_agent'])
            print(f'Authenticated successfully\n'
                  f'logged in as: {str(reddit.user.me())}')
        except Exception as e:
            print('authentication failed')
            raise
        else:
            return reddit

    def get_credentials_from_input(self):
        """ gets credentials required for authentication from user input """
        cred_dict = {}
        cred_dict['username'] = input('username: ')
        cred_dict['password'] = getpass('password (not shown when typed): ')
        cred_dict['client_id'] = input('client id: ')
        cred_dict['client_secret'] = input('client secret: ')
        cred_dict['user_agent'] = input('user agent: ')
        return cred_dict

    def get_credentials_from_file(self, file_name):
        """ gets credentials required for authentication from file """
        cred_dict = {}
        with open(file_name, "r") as file:
            for line in file.readlines():
                temp = "".join(line.split()).split('=')
                cred_dict[str(temp[0])] = str(temp[1])
        return cred_dict

    def notify(self, submission):
        """ notifies all subscribed users on subscription list about posted submission """
        for redditor in self.db['subscribers']:
            # message that is send to subscribers:
            self.reddit.redditor(redditor).message(
                # subject:
                'New paid submission posted in ' +
                str(submission.subreddit),
                # body:
                'New paid submission posted by u/' +
                str(submission.author) + ' in ' +
                str(submission.subreddit) + '\n\n'
                'Direct link: ' + str(submission.shortlink) + '\n\n\n'
                '*^I ^am ^a ^bot, ^bleep, ^bloop*')


if __name__ == "__main__":
    bot = RedditBot()
    bot.main()
