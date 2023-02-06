# se23-project2
Basic continuous integration server for course DD2480

## CI Server v0.1.0

### Installation and use

With python (>=3.7) installed, clone the repository. 

#### Dependencies

Install dependencies with `pip install -r src/requirements.txt`.
Depending on your machine, you may need to use `pip3`.

[Ngrok](https://ngrok.com/) is the recommended option for hosting the public facing server.

#### Use

To activate the CI when already hosted, push a change to the repository.

Run the server with `flask --app src/main/server.py run -p {PORT}` from the root directory.

To host the server yourself, use `ngrok http {PORT}` and copy the forwarding URL into a GitHub webhook.