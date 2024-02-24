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

To get help:

```
punch -h
```

To get help for a specific command:

```
punch COMMAND -h
```

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