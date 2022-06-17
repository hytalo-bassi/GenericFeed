# GenericFeed ![hits](https://hits.dwyl.com/Luska1331/hits.svg)
Generic Feed - Bot designed to update you on the news.

Project still under development, feel free to contribute to it.

> If you want to see how the bot works in practice, join [my Telegram group](https://t.me/LuskaHub) and call me (Same name as Github xD)

# Runnning

### Requirements

- MongoDB
- Python 3.10
- Telegram API Secrets
- Bot Token

*using docker*

- Docker CLI
- Docker Compose

#### Getting the API Secrets and Bot Token

Go to https://my.telegram.org/, log in and click at API Development Tools. Then, run this command:


```
export API_ID=<API_ID>
export API_HASH=<API_HASH>
```

After that, send `/start` to [@BotFather](https://t.me/BotFather) and `/newbot`.
When the process end, copy the API Token(it should looks like `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`) and run this command:

```
export BOT_TOKEN=<BOT_TOKEN>
```

*If you want to save this to an environment file, run:*

```
echo "export API_ID=$API_ID
export API_HASH=$API_HASH
export BOT_TOKEN=$BOT_TOKEN" >> .env
```
### Start

```
export MONGODB_URI=mongodb://127.0.0.1:27017
python -m GenericFeed
```
