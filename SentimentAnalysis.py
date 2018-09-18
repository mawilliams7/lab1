"""
CS 2302
Mark Williams
Lab 1
Diego Aguirre/Manoj Saha
9-8-18
Purpose: Use recursion to traverse a Reddit comment tree for positive,
negative, and neutral comments.
"""

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw
import datetime
import collections

ALL_COMMENT_DICT = {}
ALL_LIST = []

POSITIVE_COMMENT_DICT = {}
POSITIVE_LIST = []

NEGATIVE_COMMENT_DICT = {}
NEGATIVE_LIST = []

reddit = praw.Reddit(client_id='sNEpJsvAP2KH3A',
                     client_secret='Hwp1J1BCZXWZ68o_7S-7czQq5Yo',
                     user_agent='my user agent'
                     )

sid = SentimentIntensityAnalyzer()


def get_text_negative_proba(text):
  return sid.polarity_scores(text)['neg']


def get_text_neutral_proba(text):
  return sid.polarity_scores(text)['neu']


def get_text_positive_proba(text):
  return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
  submission = reddit.submission(url=url)
  submission.comments.replace_more()

  return submission.comments


def process_comments(comments, i):
  """
  Processes a tree of comments from a Reddit url and separates them into
  three bins: negative, neutral, positive.
  
  Args:
    comments: A CommentForest object that contains the comment tree from
    a Reddit url
    i: The iterator used for the recursive calls
  
  Returns:
    negative_comments_list : A list of PRAW comment objects that are 
			     rated as negative
    neutral_comments_list : A list of PRAW comment objects that are 
			    rated as neutral
    positive_comments_list : A list of PRAW comment objects that are 
			     rated as positive

  """
  if not comments or i >= len(comments):
    return [], [], []
  negative_comments_list = []
  neutral_comments_list = []
  positive_comments_list = []
  neg = get_text_negative_proba(comments[i].body)
  neu = get_text_neutral_proba(comments[i].body)
  pos = get_text_positive_proba(comments[i].body)
  # The criteria for separating comments into the three bins
  if neg > neu and neg > pos: 
    negative_comments_list.append(comments[i])
  elif neu > neg and neu > pos: 
    neutral_comments_list.append(comments[i])
  elif pos > neg and pos > neu: 
    positive_comments_list.append(comments[i])
  else:
    neutral_comments_list.append(comments[i])
  # If a comment has replies, this block processes the first reply
  if comments[i].replies:
    negative_extension, neutral_extension, positive_extension = \
        process_comments(comments[i].replies, 0)
    negative_comments_list.extend(negative_extension)
    neutral_comments_list.extend(neutral_extension)
    positive_comments_list.extend(positive_extension)
  # Process the next comment in that level of comments
  negative_extension, neutral_extension, positive_extension = \
      process_comments(comments, i+1)
  negative_comments_list.extend(negative_extension)
  neutral_comments_list.extend(neutral_extension)
  positive_comments_list.extend(positive_extension)
  
  return negative_comments_list, neutral_comments_list, positive_comments_list


def create_comment_dict_list(comments):
  """
  Creates a dictionary of date, comment pairs and a list of comment dates.
  
  Args:
    comments: A list of Comment objects
  
  Returns:
    date_comment_dict: A dictionary where the key is a date in the form
    of an integer and the value is a Comment object
    date_list : A list of dates that are integers

  """
  date_comment_dict = {}
  date_list = []
  for comment in comments:
    date_comment_dict[comment.created] = comment
    date_list.append(comment.created)
  date_list = sorted(date_list)
  return date_comment_dict, date_list


def get_oldest_comment_any():
  """
  Retrieves the oldest comment from a Reddit post.
  
  Args:
    None
  
  Returns:
    oldest_comment.body: The text body of a comment object

  """
  if not ALL_LIST:
    return ("There are no comments left to extract.")
  oldest_comment = ALL_COMMENT_DICT[ALL_LIST[0]]
  del ALL_LIST[0]
  return oldest_comment.body

def get_oldest_positive_comment():
  """
  Retrieves the oldest positive comment from a Reddit post.
  
  Args:
    None
  
  Returns:
    oldest_comment.body: The text body of a comment object

  """
  if not POSITIVE_LIST:
    return ("There are no comments left to extract.")
  oldest_comment = POSITIVE_COMMENT_DICT[POSITIVE_LIST[0]]
  del POSITIVE_LIST[0]
  return oldest_comment.body

def get_oldest_negative_comment():
  """
  Retrieves the oldest negative comment from a Reddit post.
  
  Args:
    None
  
  Returns:
    oldest_comment.body: The text body of a comment object

  """
  if not NEGATIVE_LIST:
    return ("There are no comments left to extract.")
  oldest_comment = NEGATIVE_COMMENT_DICT[NEGATIVE_LIST[0]]
  del NEGATIVE_LIST[0]
  return oldest_comment.body


def main():
  test_urls = ['https://www.reddit.com/r/ProgrammerHumor/comments/85a6n7/gru_tries_recursion/',
               'https://www.reddit.com/r/AstralProjection/comments/8u4e6k/ive_been_blind_since_birth_here_are_my_astral/',
	       'https://www.reddit.com/r/Music/comments/9dh89z/the_cranberries_singer_dolores_oriordan_died_by/',
	       'https://www.reddit.com/r/pcmasterrace/comments/98wmdt/with_the_new_nvidia_gpus_announced_i_think_this/',
	       'https://www.reddit.com/r/NYTauto/comments/8ld42b/local_geoffrey_hendricks_86_attentiongetting/']
  # Creates the global variables necessary for getting oldest comment
  global ALL_COMMENT_DICT
  global ALL_LIST
  global NEGATIVE_COMMENT_DICT
  global NEGATIVE_LIST
  global POSITIVE_COMMENT_DICT
  global POSITIVE_LIST
  # Iterates through the test urls and displays info about each
  for post_url in test_urls:

    ALL_COMMENT_DICT = {}
    ALL_LIST = []
    NEGATIVE_COMMENT_DICT = {}
    NEGATIVE_LIST = []
    POSITIVE_COMMENT_DICT = {}
    POSITIVE_LIST = []

    comments = get_submission_comments(post_url)
    print("We are looking at the post with url: " + post_url + "\n")
    negative_comments_list, neutral_comments_list, positive_comments_list = \
	process_comments(comments, 0)
    
    all_comments_list = []
    for comment in positive_comments_list:
      all_comments_list.append(comment)
    for comment in neutral_comments_list:
      all_comments_list.append(comment)
    for comment in negative_comments_list:
      all_comments_list.append(comment)
   
    all_comment_dict, all_list = \
	create_comment_dict_list(all_comments_list)
    ALL_COMMENT_DICT = all_comment_dict
    ALL_LIST = all_list
    
    positive_comment_dict, positive_list = \
	create_comment_dict_list(positive_comments_list)
    POSITIVE_COMMENT_DICT = positive_comment_dict
    POSITIVE_LIST = positive_list

    negative_comment_dict, negative_list = \
      create_comment_dict_list(negative_comments_list)
    NEGATIVE_COMMENT_DICT = negative_comment_dict
    NEGATIVE_LIST = negative_list

    print("The total number of negative comments in this post are: " 
	+ str(len(negative_comments_list)))
    print("The total number of neutral comments in this post are: " 
	+ str(len(neutral_comments_list)))
    print("The total number of positive comments in this post are: " 
	+ str(len(positive_comments_list)) + "\n")

    print("The oldest comment in this post is: ")
    print(get_oldest_comment_any() + "\n")
    print("The second oldest comment in this post is: ")
    print(get_oldest_comment_any() + "\n")
    print("The oldest positve comment in this post is: ")
    print(get_oldest_positive_comment() + "\n")
    print("The oldest negative comment in this post is: ")
    print(get_oldest_negative_comment() + "\n")

    #print("The oldest negative comment in this post is: ", get_oldest_negative_comment(), "\n")


main()
