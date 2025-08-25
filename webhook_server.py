from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Flask webhook server is running.', 200

@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.json

    # Extract useful info from push event
    repo_name = data.get('repository', {}).get('full_name')
    pusher = data.get('pusher', {}).get('name')
    commits = data.get('commits', [])

    print(f"Push event received from repo: {repo_name}")
    print(f"Pusher: {pusher}")
    print("Commits:")
    for commit in commits:
        print(f"- {commit.get('message')} by {commit.get('author', {}).get('name')}")

    return '', 200

if __name__ == '__main__':
    app.run(port=5000)
