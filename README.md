# slackbot-resource-queue
A Slack bot to manage resource queues

## Prerequisite
* Account created w/ Slack and membership to a workspace
* Bot created and configured and joined a workspace
* Know the **API token** and **ID** of the bot (run the `print_user_ids.py` script if necessary)
* Python 3.x and `pipenv` installed

## Set up
* Set these environment variables:
  * `BOT_ID` - The ID for the bot 
  * `BOT_API_TOKEN` - The API token for the bot to use
  
Windows example:
```
set BOT_ID=A212356C
set BOT_API_TOKEN=xobx-1133333544-a34ecde123656546
```

If the bot ID is not known, try running this (setting the environment variable `BOT_API_TOKEN` is still required):
```
pipenv run python print_user_ids.py
```

## Updating requirements.txt
The project uses Pipfile. However, Github's actions currently expects the older `requirements.txt`. Run this 
after updating dependencies with `pipenv`:

```
pipenv run pip freeze > requirements.txt
```

  
## Running
```
pipenv run python slackbot.py
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

NOTE: some pieces of that screen cap is inaccurate/missing; I'm in the process of adding the missing pieces.
