# Video-Desktop-Background
Simple python program to set a video as your Windows desktop background.


## How to use
- You should have python installed on your system
- Put the main.pyw file anywhere you like
- Put the video(s) you want to be played in the same folder
- Run the file by double clicking on .pyw file (first run for each video takes a while (~1min for a 30 seconds video)
- The script will choose a video randomly

## How to make it run automatically

### autorun with task scheduler
- Open Windows Task Scheduler
- Create a new task, make it run everytime system turns on
- Enter these when you are asked:
- command: `pythonw`
- Arguments: `"Path\To\Script\main.pyw"` (With Quotes)
- Working Directory: `Path\To\Script` (Without Quotes)
- And The script will automatically run!

### autorun with startup
- Create a bat file that runs the script with the command `start /b pythonw "Path\To\Script\main.pyw"`
- Hit Win+R
- Type shell:startup
- Place the .bat file in the opened folder
- The Script will run next time you turn on you log in!

This script was written just for the fun of it, so it may contain bugs and other problems.
You should use the amazing app [Lively](https://github.com/rocksdanister/lively).
