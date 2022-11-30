from fastapi import FastAPI, HTTPException, Response
from public import PUB_KEY


app = FastAPI()

USERNAME = ''
DOMAIN = ''
ACCT = '@{}'.format(USERNAME, DOMAIN)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/.well-known/webfinger')
async def webfinger(resource: str, response: Response):
    if resource != "acct:{}".format(ACCT):
        raise HTTPException(status_code=404, detail="Item not found")

    resp = {
        "subject": "acct:{}".format(ACCT),
        "links": [
            {
                "rel": "self",
                "type": "application/activity+json",
                "href": "https://{}/users/".format(DOMAIN, USERNAME)
            }
        ]
    }

    response.headers['Content-Type'] = 'application/jrd+json'
    return resp


@app.get('/users/{username}')
async def user(username: str, response: Response):
    if username != USERNAME:
        raise HTTPException(status_code=404, detail="User not found")

    resp = {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/v1",
        ],
        "id": "https://{}/users/{}".format(DOMAIN),
        "inbox": "https://{}/users/{}/inbox".format(DOMAIN, USERNAME),
        "outbox": "https://{}/users/{}/outbox".format(DOMAIN, USERNAME),
        "type": "Person",
        "name": USERNAME,
        "preferredUsername": USERNAME,
        "publicKey": {
            "id": "https://{}/users/{}#main-key".format(DOMAIN, USERNAME),
            "id": "https://{}/users/{}".format(DOMAIN, USERNAME),
            "publicKeyPem": PUB_KEY
        }
    }

    # Servers may discard the result if you do not set the appropriate content type
    response.headers['Content-Type'] = 'application/activity+json'
    return resp


@app.post('/users/<username>/inbox')
async def user_inbox(username):
    if username != USERNAME:
        raise HTTPException(status_code=404, detail="User not found")

    return {}
