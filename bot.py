import praw

def run_stream(stream, handler):
    for item in stream:
        if item is None:
            break
        handler(item)

def inbox_handler(message):
    """ handles new personal messages """
    print(message.author, message.body)

def submission_handler(submission):
    """ handles new posts """
    print(submission.title)

cred_dict = {}
file = open ("cred.txt", "r")
for line in file.readlines():
    temp = line.replace('\t', '').replace(' ', '').strip().split('=')
    cred_dict[str(temp[0])] = str(temp[1])

reddit = praw.Reddit(client_id=cred_dict['client_id'],
                     client_secret=cred_dict['client_secret'], password=cred_dict['password'],
                     user_agent=cred_dict['user_agent'], username=cred_dict['username'])

subreddit = reddit.subreddit('PhotoshopRequest')

inbox_stream = reddit.inbox.stream(pause_after=-1)
submission_stream = subreddit.stream.submissions(pause_after=-1)

while True:
    run_stream(inbox_stream, inbox_handler)
    run_stream(submission_stream, submission_handler)
