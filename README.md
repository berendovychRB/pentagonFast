## It's project for practice FastApi Framework.
### Project provides:
* Methods CRUD
* Login (JWT Authentication)
* Simple Registration (Check unique email and length password)
---
### For test project clone project on local repository you need to install <poetry>
#### osx / linux / bashonwindows install instructions
> curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
#### windows powershell install instructions
> (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -

### Now you need to install dependencies
> poetry install
---
### For running this with Docker:
* Make sure you have docker installed and running on your machine.
* Open the terminal to the docker-compose path and hit the following command:
> docker-compose up --build