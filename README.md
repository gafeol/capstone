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

OK, agora acho que auth0 ta configurado pra responder com token.
Porém, como que faço para receber esse token da capstone api, dado que usuário se logou na Application capstone.

Tendo erros na hora de autenticar na capstone.

LER ISSO:
https://auth0.com/docs/tokens/management-api-access-tokens/get-management-api-access-tokens-for-production


LER 
https://knowledge.udacity.com/questions/118969

## DEBUG

- If OAuth is not doing the authentication correctly, check if the AUTH0_SECRET is really accessible by the code.
