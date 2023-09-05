# Matrix reddit Bot
Matrix bot which listens to matrix messages and scans for links and commands. If link contains reddit media then it scrapes the link and downloads it to tha local machine. 

### Usage
`export MATRIX_SERVER=<matrix home server address>`

`export REDITBOTUNAME=<matrix user name>`

`export REDITPASSWORD=<matrix password>`

`python bot.py`

### Bot commands
command should start with `!`, link does not required to be start with `!`

Example commands:

`shutup bot` silences bot for random number of messages.

`!<message>` replies the same message.

Media is stored under directory `~/.cache/ReditBot/Download/`
