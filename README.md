# Project Purpose #
- Create a simple Python Version Manager
- Allow users to easily switch between multiple versions of Python
- Manage global and local Python versions for projects

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

# POC # 
- Considering this a POC for the time being
- If I want this to truly manage all my python installs vs needing global ones 
  - I should probably build this WITHOUT Python, but good for fast prototyping
  - might look into building a .NET console app if everything looks good

# TODOS # 
- An install/setup script file will need to be built to setup pvm on first use
  - it should create the pvm folder structure in the user's home directory
  - it should probably install a default python version
  - it will need to add the global python version to users PATH (globally)
- This will add complexity but is necessary for full version management
- Need to start grabbing users OS/CPU Architecture to download correct python builds