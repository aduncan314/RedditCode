# RedditCode
Some functions for accessing Reddit using PRAW
## Football.py
Currently posts top Reddit submissions from /r/patriots along with highest comment. Eventually this will work to help those of us that are football illiterate speak to those that are True Fans as seen in "The IT Crowd".

### Example

After setting up for configuration file, run
```Bash
python Football.py
```

Create a file called "config" using the following template:

```
#Configuration file for Reddit API access through PRAW
[data-collector-personal]
client_id: '<your_client_id*>'
client_secret: '<your_client_secret*>'
user_agent: '<your_user_agent>'
username: '<your_username**>'
password: '<your_password**>'
~                                          
```
\*All fields with an asterisk must be taken from your Reddit account when you set up as a developer

\**These fields are only needed for "authorized" actions like posting, voting, etc.# RedditCode
Some functions for accessing Reddit using PRAW
