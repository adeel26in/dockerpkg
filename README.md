dockerpkg

A simple package manager–like CLI tool for Docker, written in Python and easy to install. (Inspired by Linux package managers)

---

Installation (MacOS and Windows):

# Install pipx if not installed
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install dockerpkg
pipx install --system-site-packages git+https://github.com/adeel26in/dockerpkg.git

# Test
dockerpkg help

Installation (Linux):

# 1. Create a virtual environment
python3 -m venv ~/dockerpkg-venv

# 2. Activate the environment
source ~/dockerpkg-venv/bin/activate

# 3. Install dockerpkg
pip install git+https://github.com/adeel26in/dockerpkg.git

# 4. Test
dockerpkg help

Uninstallation (MacOS and Windows):

pipx uninstall dockerpkg

Uninstallation (Linux):

rm -rf ~/dockerpkg-venv

