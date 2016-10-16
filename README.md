# silverplate

## Installation

Working with python, required is to have python installed and to use
virtualenv. To do so, install them (for Fedora below)

```sh
sudo dnf install -y python3 python3-devel python3-pip postgresql-devel rpm-build
sudo pip install virtualenv
```

Next you need to move to project directory and install requirements

```sh
cd /path/to/project/directory
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Template

We have used for development a startbootstrap business casual template
which is on MIT license.
