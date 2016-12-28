# CMS Bot
This method of Installation and setting up is done on Windows 
## Installation
There are three steps
* Deploying `cmsbot` folder on Heroku
* Setting up Messenger Bot
* Setting up python script for getting CMS notices

### Deploying `cmsbot` folder on Heroku

* Before deploying, enter some random string in `cmsbot/app.js` on `line 14` replacing `<verify_token_here>`. Remember this string, we will use it later.
* Details on how to deploy are clearly given in Heroku website [here](https://devcenter.heroku.com/articles/getting-started-with-nodejs). Just follow all the steps.

### Setting up Messenger Bot

* Before you proceed to create an app for Messenger, make sure you have a Facebook page.
* Go to https://developers.facebook.com. Click `My apps` on the top right hand corner and then click `Add a New App`. Fill in the details and choose category as `Apps for Messenger` and click `Create App ID`
* In the resulting page, scroll down and click `Setup Webhooks` under Webhooks section.
* Under the `Callback URL`, enter the URL of the web app you deployed on Heroku followed by `/webhook`. Ex: `http://exampleapp.herokuapp.com/webhook`
* Under `Verify token`, enter the same string you entered in `cmsbot/app.js` on `line 14`.
* Check all except `messaging_payments` and Submit.
* You should get green complete symbol if every thing till this point is successful under `webhooks` section.
* Under webhooks, Select a Facebook page and then click `Subscribe`.
* In the `Token Generation` section, select the same Facebook page as above and copy the generated `Page Access Token`.
* Paste the `Page Access Token` in `cmsbot/app.js` on `line 122` replacing `process.env.CMS_FB_ACCESS_TOKEN` and recommit the changes to Heroku.
* Paste the same `Page Access Token` in `main.py` replacing `os.environ['CMS_FB_ACCESS_TOKEN']` on `line 13`.
* This should be sufficient for now, Go to your facebook page and send the facebook page a message. If everything went well, it should echo back the same message.
* Go to your heroku dashboard, open `View logs` for your app and search for the line starting with `Received message for user.....`. The number after `user` is your `receipient Id`. Note it down.

### Setting up python script for getting CMS notices

* Go to `main.py` `line 20` and replace the value of `id` with the `receipient Id` you obtained above.
* Replace `line 66` and `line 67` with you CMS username and password.
* Everything done. Now, run `main.py`. Before you run, install `selenium` and `colorama` in python, if you don't have already. Now, all you notices will be saved in database and you will get those notices as messages in your Facebook account. For the first run, all your notices will sent to you. For the secind time onwards, only new notices will be sent to you. You can run the script hourly by creating a batch file or host it in `pythonanywhere`.
