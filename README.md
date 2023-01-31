# Typing Speed Tester

![Typing Speed Tester's screenshot](https://raw.githubusercontent.com/cihatertem/typing_speed_thinker/master/screenshot.png)
A simple typing speed test tool based on Python/Tkinter.

## Features

- Top 3000 English words data source
  from [EF](https://www.ef.com/wwen/english-resources/english-vocabulary/top-3000-words/).
- Test duration 60s fixed for now.
- WPM (word per minute) and failed words counter
- Test score screen

## Upcoming Features (Maybe :) )

- Turkish support
- CPM(character per minute)
- Theme / Style
- Test duration options
- Typing sound
- Score to data
- Users' credentials
- Focus mode
- Possible bug fixes.

## Requirements

Python must be installed on your system.
To recreate word_list.json data, Python's Beautifulsoup4 and Requests libraries are required.

```shell
pip install -r requirements.txt
```

## Start

Test time counter starts with first typing automatically.

```shell
python main.py
```

Or

```shell
python -m main
```
