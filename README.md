# Punch
Command line interface to log working hours and calculate overtime.
## Get started
Entrypoint: `punch.py`

I recommend to setup an alias in your terminal config, e.g. `alias punch='$PUNCH_DIR/punch.py'`

Run `punch -h` to get command help.

Run `punch COMMAND -h` to get help in using the different commands.

## Examples
Adding a log for today:
```
punch add 9-12
```
Adding log for Tuesday this week:
```
punch add -p Tue 9-12
```
Get logged hours of the current week and overtime:
```
punch hours
```
Remove last log of current week:
```
punch remove
```