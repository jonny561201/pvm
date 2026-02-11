# Project Purpose #
- Create a simple Python Version Manager
- Allow users to easily switch between multiple versions of Python
- Manage global and local Python versions for projects
- Will activate `venv` environments when "cd" to a project directory
- The `.python-version` file will be used to switch versions if a version is installed (venv honored first)

# Problems #
- The use of uv on Windows is limiting
- I want to avoid using a library to swallow my python commands
- I also want to keep the performance improvements of uv without the env var shims
- I want to avoid the complexity of pyenv
- I want a simple, easy to use tool that does one thing well

# Features #
- `pvm install <version>`: Install a specific version of Python
- `pvm use <version>`: Switch to a specific version of Python in local terminal
- `pvm default <version>`: Set a global default Python version
- `pvm list`: List all installed Python versions

# Structure #
- Installs in the user's home directory under `.pvm`
- Each Python version is installed under the `.pvm/versions` directory in their own subdirectory
- A symlink is created under the `.pvm/bin` directory for the active Python version, which is added to the user's PATH

# POC # 
- Considering this a POC for the time being
- If I want this to truly manage all my python installs vs needing global ones 
  - I should probably build this WITHOUT Python, but good for fast prototyping
  - might look into building a .NET console app if everything looks good

# TODOS #
- Right now it only grabs latest releases....need to support historical builds too

# Install #
- Linux / MacOS
`curl -fsSL https://raw.githubusercontent.com/jonny561201/pvm/main/install.sh -o install.sh && chmod +x install.sh && ./install.sh`

- Windows (Powershell)
`iwr -useb https://raw.githubusercontent.com/jonny561201/pvm/main/install.ps1 | iex`