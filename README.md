# Close Call

Socially embarassing wake up calls. 

http://hotlinering.com

# Setting up locally

There are four major components of the service. The Python Flask frontend, the Python core, the Redis server for handling scheduling, and the C# backend for handling Twilio.

1. Clone this repo to a directory
2. Enter the directory

Code blocks are terminal/command line commands
You may also want to check out [this](https://github.com/golf1052/close-call/commit/0564dfc8d38eb681191dbe406432ba2610f9b698) commit where we move from localhost to our website. Switch everything back to localhost using the same ports we used.

## Setting up configs
1. You need to enter the right things into config.py and caller/credentials.json to get things working right. See their respective sample files to see what they should look like.

### Facebook
TODO: No idea but you probably need something relating to [this](https://developers.facebook.com/docs/graph-api/overview/).

### Venmo
See [here](https://developer.venmo.com/gettingstarted/createapp)

### Indico
See [here](https://www.indico.io/docs)

### Mongo
See [here](https://docs.mongodb.org/manual/installation/). I wish you luck.

### Twilio
Sign up with [Twilio](https://www.twilio.com/try-twilio). Enter your SID, auth token, and Twilio phone number (formatted +14445556666 where +1 is the country code) into caller/credentials.json. You can find those [here](https://www.twilio.com/user/account/settings).

## Setting up frontend and core
1. Install [Python 2.7.x](https://www.python.org/downloads/).
2. Install [pip](https://pip.pypa.io/en/stable/installing/).
3. Install and setup a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
4. Make sure you are inside your virtualenv.
5. ```pip install -r requirements.txt```  
  5a. You may run into issues when installing Pillow. First check [here](https://indico.io/docs) then check [here](http://pillow.readthedocs.org/en/3.0.x/installation.html).
6. ```python app.py```

## Setting up Redis
1. Open a new terminal/command line window.
2. Install [Redis](http://redis.io/download).  
  2a. I haven't tested this on Windows. Hopefully it should work.  
  2b. We were running redis 2.8.6 but any version supported by python-rq should work.
3. Make sure redis-server is running.  
  3a. Try typing ```redis-cli ping```. If redis-server is running you should see PONG.

## Setting up rqscheduler
1. Open a new terminal/command line window.
2. Navigate to where you cloned the repo.
3. Enter your virtualenv for this project.
4. ```rqscheduler```  
  4a. It looks like nothing is happening. Apparently something is happening.

## Setting up rqworker
1. Open a new terminal/command line window.
2. Navigate to where you cloned the repo.
3. Enter your virtualenv for this project.
4. ```export PYTHONPATH=/path/to/where/you/cloned/this/repo/close-call```  
  4a. Basically PYTHON_PATH needs to point to the root of the project.  
  4b. This is for OS X/Linux. For Windows:
    * Open the System control panel (under System and Security)
    * Go to Advanced System Settings
    * Open Environment Variables
    * Either create PYTHONPATH or append the path (if you are appending remember to add a ```;``` between the last path
    * Example path: ```C:\path\to\where\you\cloned\this\repo\close-call```
5. rqworker

## Setting up Twilio backend
1. Open a new terminal/command line window.
2. Navigate to where you cloned the repo and then go into caller.
3. Follow the instructions [here](https://docs.asp.net/en/latest/getting-started/index.html) to set up dnvm and dnx.
4. Install/upgrade coreclr: ```dnvm upgrade -r coreclr```.
5. Make sure you are using coreclr as your runtime.  
  5a. ```dnvm list```. The latest version should have a * next to it. If not type something like: ```dnvm use 1.0.0-rc1-update1 -a x64 -r coreclr``` where 1.0.0-rc1-update1 is the latest version of the runtime.  
  5b. This is also a good time to set the latest version to your default. Type: ```dnvm alias default 1.0.0-rc1-update1 -a x64 -r coreclr``` where 1.0.0-rc1-update1 is the latest version of the runtime.
6. ```dnu update```
7. ```dnx web```

## Testing
Wow, you got everything running. Navigate to http://localhost:5000 in your browser and you should see our awesome front page. Authenticate with Facebook and/or Venmo. Enter a time before now and your phone number (area core, no dashes or parens example 4445556666). If everything was set up correctly you should receive a call. If you hang up depending on what consequence you chose something should appear on your Facebook wall (this is not visible to anyone who hasn't been authorized with your Facebook app) or money should have been sent to one of us (maybe, you may only be able to send money to friends through the Venmo API). If you enter the code then you should be prompted that the consequence has been dropped.