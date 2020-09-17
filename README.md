Make `secrets.py` with:

```
p_pass = '' # your piazza password
p_email = '' # your piazza email login
p_network = '' # the letters/numbers after /class/ in the url, https://piazza.com/class/...,
d_url = '' # discord webhook url, https://discordapp.com/api/webhooks/...
```

```
pip install aiohttp discord piazza-api
```

Crontab every 5 minutes?
```
*/5 * * * * /usr/bin/python /home/USER/PiazzaBot/PiazzaBot.py
```

Right click on server. Server settings. Integrations. Webhooks. New Webhook
