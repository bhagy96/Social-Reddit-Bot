import openai
import praw
import random
import re
from datetime import datetime
import time

def get_bot_details(bot_no):
    if bot_no =="1":
        return praw.Reddit(client_id='',
                    client_secret="",
                    username="",
                    password="",
                    user_agent="<console:SecretBot:1.0>")
    elif bot_no =="2":
        return praw.Reddit(client_id='',
                         client_secret="",
                         username="",
                         password="",
                         user_agent="<MyBot:1.0>")
    else:
        return praw.Reddit(client_id='',
                    client_secret="",
                    username=" ",
                    password="",
                    user_agent="<console:mybot3:1.0>")

def generate_response(bot_no, subr, keywords, action_lst, prompt, max_t):
    openai.api_key = "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"

    reddit = get_bot_details(bot_no)
    print("in generate response")
    no_of_interations = 10
    subreddit = reddit.subreddit(subr)

    choice = random.choice(action_lst)
    posts = subreddit.search(keywords, sort='hot', limit=2)
    action_completed = ""
    if choice=='1':
        print("upvoting")
        for post in posts:
            print(post.title)
            print(post.url)
            action_completed = "The bot has upvoted the post"
            post.upvote()
            break
    elif choice=='2':
        print("commenting")
        for post in posts:
            if prompt:
                prompt = prompt + post.title + " and with body " + post.selftext
            else:
                prompt = "Comment on the post titled " + post.title + " and with body " + post.selftext
            response = openai.Completion.create(model="text-davinci-003",prompt=prompt,temperature=0,
                                                max_tokens=max_t, top_p=1,frequency_penalty=0.5,presence_penalty=0)
            print("*******************************")
            print("post title is")
            print(post.title)
            print("post body is")
            print(post.selftext)
            print(post.url)
            print("rsponse is")
            print(response)
            post.reply(response)
            my_comment = response.choices[0].text.strip()
            action_completed = "The bot has commented on the post"
            ret_text = "Original post title:\n" + post.title + "\nComment made: \n" + my_comment

            break
    else:
        if not prompt:
            if keywords:
                prompt = 'Generate a post which would contain ' +keywords
            else:
                prompt = 'Generate a post '
        else:
            if keywords:
                prompt = prompt + " which would contain these words: " + keywords
        response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0,
                                            max_tokens=max_t, top_p=1, frequency_penalty=0.5, presence_penalty=0)

        text = response.choices[0].text.strip()
        prompt = 'Generate a title for ' + prompt
        response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0,
                                            max_tokens=10, top_p=1, frequency_penalty=0.5, presence_penalty=0)
        title = response.choices[0].text.strip()
        print(title, "\n")
        print("*******", "\n", text)
        subreddit = reddit.subreddit(subr)
        subreddit.submit(title, selftext=text)
        ret_text = "Post made: \n" + " Title : \n" + title + "\n Body: \n" + text
    return action_completed,ret_text
    # return , my_comment