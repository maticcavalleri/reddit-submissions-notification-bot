import praw

cred_dict = {}
file = open ("cred.txt", "r")
for line in file.readlines():
    temp = line.replace('\t', '').replace(' ', '').strip().split('=')
    cred_dict[str(temp[0])] = str(temp[1])

reddit = praw.Reddit(client_id=cred_dict['client_id'],
                     client_secret=cred_dict['client_secret'], password=cred_dict['password'],
                     user_agent=cred_dict['user_agent'], username=cred_dict['username'])

subreddit = reddit.subreddit('PhotoshopRequest')

for submission in subreddit.stream.submissions():
    print(submission.title)
    break
