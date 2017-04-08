## Install

Install dependencies
```
pip install -r requirement.txt
```

Set API key in your env (user your own key)
http://steamcommunity.com/dev/
```
export D2_API_KEY=83247983248793298732
```

## scraper
To fetch match basic info, run the command below, it will fetch n * 100 matches. 
By default, it will start with game #2500000000, started around 12/23/2016. After that, it will always continue the latest run.

For example, fetching 200 matches.
```
python manage.py get_match_history 2
```
