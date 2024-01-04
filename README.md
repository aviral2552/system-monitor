# System monitor - A part of Project Aradia
A collection of cross-platform system monitor scripts written in Python for logging OS, application state, networking etc.

This project is currently under initial phases of active development.

## Instructions for macOS

## Pre-requisites

You must have `xcode`, `brew` and `git` installed. 

1. To install Xcode, open terminal and type

`$ xcode-select --install`

2. To install Homebrew, open terminal and type

`$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

3. After installing Xcode Homebrew, you can install `git` by typing the following in the terminal

`$ brew install git`

4. And finally you will need python3, which can be installed by using the following command in the terminal window

`$ brew install python3`

## How to run

1. Navigate to the folder where you'd like to place the files
2. Clone the project and start logging by typing the following command

`$ git clone https://github.com/aviral2552/system-monitor.git && cd system-monitor && cd bin && python3 collect.py`
