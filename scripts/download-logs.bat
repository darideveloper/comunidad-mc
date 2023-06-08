Rem download logs from heroku
del ..\.log
heroku ps:copy .log --app comunidadmc --output ../.log