# RedditCode
Some functions for accessing Reddit using PRAW
*Note:* if you stumble upon this and wonder, yes, most of this code could be written as simple on or two file scripts
intead of as a OO project with logging etc. I am using it to practice/learn design principles using a simple project
that would be more important in a larger project.

## RedditCollectionService
This is a bad name

### Example
None yet

Create a file called "config.json" using the following template:
```
{
  "default": {
    "client_id": "<your_client_id*>",
    "client_secret": "<your_client_secret*>",
    "user_agent": "<your_user_agent>"  --eg. "home:my-collector:v1.0",
    "username": "<your_username**>",
    "password": "<your_password**>"
  }
}
```

\*All fields with an asterisk must be taken from your Reddit account when you set up as a developer

\**These fields are only needed for "authorized" actions like posting, voting, etc.# RedditCode
Some functions for accessing Reddit using PRAW
