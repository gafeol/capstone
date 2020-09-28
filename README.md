# Capstone project

## Set up

To install the project dependencies, run `pip install -r requirements.txt`.

By running:

```bash
source ./setup.sh
```

You'll have configured the dev configuration for the environment variables required by Flask.

Later running:

```bash
flask run
```

Shall start the project in Debug mode.

## TODO

- Create Postman API tests
- Create db relationship between actors and movies
- Adds require auth for API
- Create decorator to check for permissions

Fazer request GET para 
https://dev-ingcvevp.us.auth0.com/authorize?audience=http://localhost:5000&response_type=token&client_id=1N0NSObu0BtQ0sMh6CRDcVRnzbqLc1ls&redirect_uri=http://localhost:5000/callback
https://dev-ingcvevp.us.auth0.com/authorize?audience=http://127.0.0.1:5000/&response_type=token&client_id=1N0NSObu0BtQ0sMh6CRDcVRnzbqLc1ls&redirect_uri=http://localhost:5000/callback

## DEBUG

- If OAuth is not doing the authentication correctly, check if the AUTH0_SECRET is really accessible by the code.
