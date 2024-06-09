from flask import Flask, render_template, request
import asyncio
import os
import twitter

app = Flask('app')

#$env:TWITTER_AUTH_TOKEN="your_auth_token"
auth_token = os.getenv("TWITTER_AUTH_TOKEN")

twitter_account = twitter.Account(auth_token=auth_token)

async def get_friends(screen_name):
    async with twitter.Client(twitter_account) as twitter_client:
        user = await twitter_client.request_user_by_username(screen_name)
        followings = await twitter_client.request_followings(user.id)
    return followings

@app.route('/', methods=['GET', 'POST'])
def home():
    friends = []
    if request.method == 'POST':
        screen_name = request.form['screen_name']
        friends = asyncio.run(get_friends(screen_name))
    return render_template('home.html', friends=friends)

def run():
    app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    run()