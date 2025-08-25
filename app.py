from flask import Flask, request
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET'])
def home():
    return 'Flask webhook server is running.', 200

@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    if event_type == 'push':
        repo_name = data.get('repository', {}).get('full_name')
        pusher = data.get('pusher', {}).get('name')
        commits = data.get('commits', [])
        logging.info(f"Push event received from repo: {repo_name}")
        logging.info(f"Pusher: {pusher}")
        logging.info("Commits:")
        for commit in commits:
            logging.info(f"- {commit.get('message')} by {commit.get('author', {}).get('name')}")

    elif event_type == 'pull_request':
        action = data.get('action')
        pr_title = data.get('pull_request', {}).get('title')
        pr_user = data.get('pull_request', {}).get('user', {}).get('login')
        logging.info(f"Pull request {action}: '{pr_title}' by {pr_user}")

    else:
        logging.info(f"Unhandled event type: {event_type}")

    return f"Received {event_type} event", 200

if __name__ == '__main__':
    app.run(port=5000)
