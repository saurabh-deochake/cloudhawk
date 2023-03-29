# Runbook
## venv
If you haven't created a virtual environment yet, create one in your project directory using the following command:
```bash
$ python -m venv venv
```
This command creates a virtual environment named venv in your project directory. You can replace venv with any name you prefer.

Activate the virtual environment:

On macOS and Linux, run:

```bash
$ source venv/bin/activate
```

With the virtual environment activated, install the packages listed in the requirements.txt file using pip:

```bash
$ pip install -r requirements.txt
```

This command installs all the packages specified in the requirements.txt file into your virtual environment.

Once the installation is complete, you can run your project within the virtual environment. To deactivate the virtual environment when you're done, simply run:

```bash
$ deactivate
```
This command returns you to your system's global Python environment.