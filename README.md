# slackbot-resource-queue
A Slack bot to manage resource queues

## Prerequisite
* Account created w/ Slack and membership to a team
* Bot created and configured
* Know the token and ID of the bot
* Python and pip installed

## Set up
* Set these environment variables:
  * BOT_ID - The ID for the bot 
  * BOT_API_TOKEN - The API token for the bot to use
  
Windows example:
```
set BOT_ID=A212356C
set BOT_API_TOKEN=xobx-1133333544-a34ecde123656546
```
* Download imported modules 
  * `virtualenv` use is recommended
  * `pip install -r requirements.txt` to download prereq modules
  
## Running
### Windows
```
set PYTHONPATH=<project location>
cd <project location>
python van\slackbot.py
```

### Non-Windows
```
export PYTHONPATH=<project location>
cd <project location>
python van/slackbot.py
```

## Commands
Issuing a command to the bot takes the form of a post directed to the bot name. *Note that the bot name depends totally on the bot's configuration.*

The example below assumes the bot name `queuesem`. 

* **add x** - adds you to the resource x
* **hello** - prints hello back to you
* **help** - help message (this list)
* **remove x** - removes you from resource x
* **remove-all x** - frees up resource x
* **status** - status of resources

Sample session:

![Sample session](https://github.com/bluedenim/slackbot-resource-queue/blob/master/images/sample_session.png)
