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

You will also need to create a `src/.env` file containing a `GITHUB_ACCESS_TOKEN` variable with `repo:status` permission to set the commit status.

To run tests locally, run `python3 -m pytest` from the root directory.

## Testing 

Features were tested with one positive test case per item being tested

### Essence
Our group's adherence to the [Essence Standard](https://www.omg.org/spec/Essence/1.2/PDF) is documented in `essence.md`.


## License

MIT License

Copyright (c) 2023 Group 29

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



## Contributors

- David Kaméus 
- Minhao Ni
- Alexander Gustavsson
- Carter Smith
- Sanjin Redzepagic

## Contributions
- Sanjin Redzepagic

- Minhao Ni
    

- Alexander Gustavsson
    - Worked on the README
    - Filled out the essence.MD file and wrote a paragraph about the groups process

- Carter Smith
    - Set up pip env, Flask boilerplate
    - Implemented payload parsing in `utils.py`
    - Implemented GitHub commit status changes

- David Kaméus
    
