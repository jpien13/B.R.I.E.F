# B.R.I.E.F
Brown's Relevant Intelligence Engine for Fintech

## Testing Locally

### Setting up Virtual Environment
This codebase assumes you are using a virtual environment (venv). This is a good practice to avoid dependency conflicts. To create a virtual environment, run the following command in the root directory of the project: 

python3 -m venv venv

To activate the virtual environment, run the following command: 

source venv/bin/activate

To deactivate the virtual environment, run the following command: deactivate

Next, you will have to install all the project dependancies. I have collected all the library dependancies you would need in the requirements.txt file. To install all the dependancies, run the following command: 

pip install -r requirements.txt

You should be all set up with the venv now.

### Setting up Environment Variables
The code expects all passwords, emails, and API keys to be environment varibles (secrets) in the GitHub workflow. This is for obvious security reasons. We wouldnt want your email, password, or keys to be leaked from a public repo :( As such, you will need to set these up locally to test the code. The following are the secrets that need to be set as environemtn variables:

This assumes you are on Mac OS and sets the temporary environment variables for the email address and password.

export EMAIL_ADDRESS="your.email@gmail.com"
export EMAIL_PASSWORD="your_password"

If you wanted permanent environment variables, you would need to add them to your .bash_profile or .zshrc file. This is not recommended for security reasons. If you are on Windows, you would need to set these as environment variables in the System Properties.

