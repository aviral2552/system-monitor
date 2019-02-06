# System monitor - A part of Project Aradia
A collection of cross-platform system monitor scripts written in Python for logging OS, application state, networking etc.

This project is currently under initial phases of active development.

## Pre-requisites

You must have `brew` and `git` installed. 

To install Homebrew open terminal and type

`$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

After installing Homebrew, you can install `git` by typing the following in the terminal

`$ brew install git`

## How to run

**For macOS/Linux/Unix**
1. Navigate to the folder where you'd like to place the files
2. Clone the project and start logging by typing the following command

`$ git clone https://github.com/thelamehacker/system-monitor.git && cd system-monitor && cd bin && python3 collect.py`