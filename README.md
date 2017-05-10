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
  * BOT_TOKEN - The token for the bot
  
Windows example:
```
set BOT_ID=A234456C
set BOT_TOKEN=xobx-1133333544-a34ecdeerr656546
```
* Download imported modules 
  * `virtualenv` use is recommended
  * `pip install -r requirements.txt` to download prereq modules
  
## Running
`python van\slackbot.py` (for Windows)

## Commands
Issuing a command to the bot takes the form of a post directed to the bot name. *Note that the bot name depends totally on the bot's configuration.*

The example below assumes the bot name `queuesem`. 

* **add x** - adds you to the resource x
* **hello** - prints hello back to you
* **help** - help message (this list)
* **remove x** - removes you from resource x
* **remove-all x** - frees up resource x
* **status x, y, z, ...** - status of resources
* **status-all** - status of everything I know of

**TO DO**
Sequence for queuing up for a resource, multiple users, getting to a resource, etc.


