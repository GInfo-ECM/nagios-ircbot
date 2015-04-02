# Install

You need python and twisted.
Optional 'daemon'.

* Download irc.py and save it where ever you chose.
* Make a fifo with "mkfifo ircpipe"
* Change MyChannel, MyIRCServer and MyPipe variables in bot.py
* In /etc/nagios/misccommands.cfg add :

```
define command{
  command_name notify-by-irc
  command_line /bin/echo "$NOTIFICATIONTYPE$ $HOSTNAME$/$SERVICEDESC$ is $SERVICESTATE$: $SERVICEOUTPUT$" > /usr/home/ircbot/pipe &
}

define command{
  command_name host-notify-by-irc
  command_line /bin/echo "$NOTIFICATIONTYPE$ $HOSTNAME$ is $HOSTSTATE$: $HOSTOUTPUT$" > /usr/home/ircbot/pipe &
}
```

* Correct the path to the pipe if neccessary.
* Add the following in the contact of your choice (usually in /etc/nagios/contacts.cfg)
  service_notification_commands  notify-by-irc
  host_notification_commands  host-notify-by-irc

* You can now do "python bot.py" to start/test the bot

# To make irc.py act as a service under debian/ubuntu :

* apt-get install daemon
* edit /etc/daemon.conf, add the line "ircbot    command=/usr/bin/python /root/irc.py" with the correct path

And voila !

To start it : daemon --name ircbot
To stop it : daemon --name ircbot --stop

# Contact
You can contact me at ~~jm-lacroix@savigny.org~~ (discontinued)
Moviuro: moviuro+ircbot@gmail.com

