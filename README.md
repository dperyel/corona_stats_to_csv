A bit tired to check the world statistics manually everyday.
BTW, https://www.worldometers.info is awesome resource to get the latest statistics.

So wrote this small script to parse the data once a day. Result is stored in stats folder. My internal cornjob gets "current" stats interested to me and writes a message.

To run:
```
python parse.py
```

In case you use conda, you can create environment with all dependencies:
```
conda env create -f ./environment.yml
```
