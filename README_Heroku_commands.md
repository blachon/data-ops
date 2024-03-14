## Heroku Commands

Init session
```
$ heroku login
```

Run the app locally
```
$ heroku local -f Procfile.windows
```

Manual push to heroku branch
```
$ git push heroku main
```

Start (scale up) the app
```
$ heroku ps:scale web=1
```

Run a remote terminal on server
```
$ heroku run bash
```

Create a staging environment on heroku (impossible to deploy an app from a remote different from heroku)
```
heroku create --remote staging
```

Deploy dev branch to main on heroku
```
git push heroku testbranch:main
```

Heroku API Key is available here: https://dashboard.heroku.com/account