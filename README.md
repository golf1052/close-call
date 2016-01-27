# Close Call

Socially embarassing wake up calls. 

http://hotlinering.com

## Local Setup

There are three major components of the service. The Flask web service, the Redis server for scheduling calls, and the C# backend for interacting with Twilio.

These instructions should work for and have been tested on Ubuntu 14.04 (Linux) and OS X (10.10). They should hopefully also work for Windows but that has not been tested yet.

1. Clone this repo to a directory
2. Enter the directory

Code blocks are terminal/command line commands
You may also want to check out [this](https://github.com/golf1052/close-call/commit/0564dfc8d38eb681191dbe406432ba2610f9b698) commit where we move from localhost to our website. Switch everything back to localhost using the same ports we used.

## Configuration Information
You need to create a couple of applications and enter configuration information into `config.py` and `caller/credentials.json` to get things working right. See their respective sample files to see what they should look like.

### Facebook
[Create a developer application](https://developers.facebook.com/quickstarts/?platform=web) and then under that application create a test application. from there you can fill in `FACEBOOK_CONSUMER_KEY` as the App ID and `FACEBOOK_CONSUMER_SECRET` as the App Secret in `config.py`. Set the Site URL to your website for production or `http://localhost:5000/` for testing. This will allow you to login with Facebook, but won't actually allow posting to be seen by anyone besides yourself and other admins/testers of your developer application.

### Venmo
[Create a developer application](https://venmo.com/account/settings/developer) and set the Web Redirect URL similarly to Facebook, your website for production or `http://localhost:5000/` for testing. You can set `VENMO_CLIENT_ID` to the Application ID and `VENMO_CLIENT_SECRET` to the Application Secret. Set `VENMO_USER_IDS` to a list of Venmo User IDs to send money to. These can be obtained from the Venmo API. This will allow you to login with Venmo and send your real money away to real strangers.

### Indico
[Follow the instructions to obtain a free API key](https://www.indico.io/docs) and set `INDICO_API_KEY` in the config.

### MongoDB
[Follow the instructions here](https://docs.mongodb.org/manual/installation/) for your respective platform. Once you have the DB running, fill in the `MONGO_HOST`, `MONGO_USER`, `MONGO_PASS`, and `MONGO_DB` values in the configuration with your host, username, password, and collection to store user data in respectively. I wish you luck.

### Twilio
Sign up with [Twilio](https://www.twilio.com/try-twilio). Enter your SID, auth token, and Twilio phone number (formatted +14445556666 where +1 is the country code) into caller/credentials.json. You can find those [in your Twilio settings](https://www.twilio.com/user/account/settings).

## Application Setup

### Flask
1. Install [Python 2.7.x](https://www.python.org/downloads/).
2. Install or upgrade [pip](https://pip.pypa.io/en/stable/installing/) if needed.
3. Install [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) via pip and create a virtual environment for this project.
4. Activate the virtual environment with `source <virualenv>/bin/activate`
5. ```pip install -r requirements.txt```  
  - You may run into issues when installing Pillow. The [Indico API docs](https://indico.io/docs#install_issues) have advice on common installation issues. Pillow also has [installation instructions](http://pillow.readthedocs.org/en/3.0.x/installation.html) that might be helpful.
6. Run ```python app.py``` to start the Flask server that runs the app.

### Redis
1. Open a new terminal window.
2. Install [Redis](http://redis.io/download).  
  a. I haven't tested this on Windows. Hopefully it should work. Take a look at [this](https://github.com/MSOpenTech/Redis).  
  b. We were running Redis 2.8.6 but any version supported by `python-rq` should work.
3. Make sure `redis-server` is running by typing ```redis-cli ping```. If it is you should see `PONG` as a response.

### rqscheduler
1. Open a new terminal window.
2. Navigate to where you cloned the repo.
3. Enter your virtualenv for this project.
4. Run ```rqscheduler```, it will look like nothing is happening. Apparently something is happening.

### rqworker
1. Open a new terminal window.
2. Navigate to where you cloned the repo.
3. Enter your virtualenv for this project.
4. Point the `PYTHONPATH` environment variable to the root of the project by doing ```export PYTHONPATH=/path/to/where/you/cloned/this/repo/close-call```  
  - For Windows:
    * Open the System control panel (under System and Security)
    * Go to Advanced System Settings
    * Open Environment Variables
    * Either create PYTHONPATH or append the path (if you are appending remember to add a ```;``` between the last path
    * Example path: ```C:\path\to\where\you\cloned\this\repo\close-call```
5. Run ```rqworker```

### Twilio backend
1. Open a new terminal line window.
2. Navigate to where you cloned the repo and then go into caller.
3. Follow the instructions [here](https://docs.asp.net/en/latest/getting-started/index.html) to set up dnvm and dnx.
4. Install/upgrade coreclr: ```dnvm upgrade -r coreclr```.
5. Make sure you are using coreclr as your runtime.  
  a. ```dnvm list```. The latest version should have a * next to it. If not type something like: ```dnvm use 1.0.0-rc1-update1 -a x64 -r coreclr``` where 1.0.0-rc1-update1 is the latest version of the runtime.  
  b. This is also a good time to set the latest version to your default. Type: ```dnvm alias default 1.0.0-rc1-update1 -a x64 -r coreclr``` where 1.0.0-rc1-update1 is the latest version of the runtime.
6. ```dnu update```
7. ```dnx web```

## Testing
Wow, you got everything running. Navigate to [http://localhost:5000/](http://localhost:5000/) in your browser and you should see our awesome front page. Authenticate with Facebook and/or Venmo. Enter a time before now and your phone number (area core, no dashes or parens example 4445556666). If everything was set up correctly you should receive a call. If you hang up depending on what consequence you chose something should appear on your Facebook wall (this is not visible to anyone who hasn't been authorized with your Facebook app) or money should have been sent to one of us (maybe, you may only be able to send money to friends through the Venmo API). If you enter the code then you should be prompted that the consequence has been dropped.
