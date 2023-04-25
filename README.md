

# Welcome to Rattlers Unite!

Rattlers Unite is a event tracking site made for [St. Mary's University](https://stmarytx.edu) as part of the Spring 2023 Semester for Dr. Redfield's CS3340/CS6340 Software Engineering class.

## Purpose

The purpose of this site is to host events and organizations on campus in a more elegant fashion compared to the current university event system (via EMS Master Calendar) and provide an incentive into partaking in these events with points and a leaderboard!

## Features
1. Point System
   > Gather points by attending events by creating an account and providing your ID number. (Execution-wise, this is determined by your St. Mary's ID number on campus along with Gateway SSO to login to your account on Rattlers Unite)
2. Leaderboards
   > Climb the ranks in order to be in the top ten or be first amongst your peers by attending events and earning points!
3. Event Tracking
   > See all current and future events that will be happening either on-campus or off-campus!
4. Organization/Event information pages
   > Get detailed information about an organization and it's events that it host or about the event you want to attend itself!
5. Organization/Admin Portal
   > Manage your events and organization profile all in one place!
6. Login/Sign Up
   > (This would be replaced with a Gateway SSO and Gateway credentials execution-wise) Register for a Rattlers Unite account as either a student or organization and login to Rattlers Unite using your credentials.

## Requirements
The requirements to run Rattlers Unite are as follows.
1. A Windows 10 or 11 PC.
2. [Python 3.11.1](https://www.python.org/downloads/release/python-3111/)
3. [Git](https://git-scm.com/)
4. [Visual Studio Code](https://code.visualstudio.com)
5. [DB Browser for SQLite](https://sqlitebrowser.org/dl/)
6. Chrome or any Chromium based browser (Brave, Microsoft Edge, etc.)

## Installation
1. Make sure you have downloaded and installed all the requirements listed in [Requirements](#requirements).
2. Open *Git* in a location you want to save Rattlers Unite.
3. Run the following command
   ```sh
   git clone https://github.com/Rattlers-Unite/RattlersUnite-System
   ```
4. Open *Visual Studio Code* and click <u>File -> Open Folder</u> and select the Rattlers Unite folder you got from *Git*.
5. Install the Python extension by going to <u>Extensions</u> and searching Python.
6. Click <u>View -> Command Pallete</u> and type the following
   > Python: Create Environment
7. Select the *.venv* environment type when prompted to select an environment type.
8. Select *Python 3.11.1 64-bit* when prompted to select a interpreter.
9. Tick *requirements.txt* under <u>Select dependencies to install</u>, then press OK.
10. After you finished installing the virtual environment, make sure the interpreter on the bottom right of Visual Studio code says 3.11.1 ('.venv', venv).
11. Click *Run -> Run With Debugging* or *Run -> Run without Debugging and visit the site at the following address.
   > http://127.0.0.1:5000

Copyright © 2023 Rattlers Unite Team. All rights reserved