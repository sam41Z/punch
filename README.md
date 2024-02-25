# Punch

Command line interface to log working hours and calculate overtime.

## Requirements

Install dependencies:

```
pip install -r requirements.txt
```

## Get started

Entrypoint: `punch.py`

I recommend to setup an alias in your terminal config, e.g. `alias punch='$PUNCH_DIR/punch.py'`

Without arguments the app launches in interactive mode. Available functions are:
* __add__ time records
* __remove__ previously added time records
* get the breakdown of a specific week, referred to as __hours__

__Hint__: Letters in brackets, e.g. `[a]` can be used as shortcuts. 

### Commandline Arguments
For quick access a few functions are available through a command line arguments.
#### Adding records
For today: 
```
punch add 9-12
```
For any day in the week, using the prefix option `-p`
```
punch add -p Tue 9-12
```
#### Hours of current week
Get logged hours of the current week and overtime:

```
punch hours
```

