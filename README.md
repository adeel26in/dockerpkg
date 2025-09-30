dockerpkg

A simple package manager–like CLI tool for Docker, written in Python and easy to install. (Inspired by Linux package managers)

---


- Python 3.8+ installed
- Docker installed and running
- On Linux, make sure your user can run Docker without sudo: docker ps


# Installation (MacOS and Windows):

python3 -m pip install --user pipx
python3 -m pipx ensurepath

pipx install --system-site-packages git+https://github.com/adeel26in/dockerpkg.git

dockerpkg help

# Installation (Linux):

python3 -m venv ~/dockerpkg-venv

source ~/dockerpkg-venv/bin/activate

pip install git+https://github.com/adeel26in/dockerpkg.git

dockerpkg help

Optional: Add an alias for easy access (Chaneg bashrc if using zsh):

echo 'alias dockerpkg="~/dockerpkg-venv/bin/dockerpkg"' >> ~/.bashrc

source ~/.bashrc

# Uninstallation (MacOS and Windows):

pipx uninstall dockerpkg

# Uninstallation (Linux):

rm -rf ~/dockerpkg-venv

