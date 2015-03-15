## BuildBot ##

[BuildBot](http://buildbot.net/) is an awesome automatic build and testing tool. It will sit and look for changes to your source-code repository and upon detecting a change, it will perform a build and run the test suite (assuming you have one of course). This **automated** building and testing  can help developers ensure that they have not inadvertently broken the build by committing bad code into the repository. Of course developers should build and test their changes before they get committed at all(!), but sometimes, in the heat of coding, this can be easy to forget. However there are also more complex scenarios, where a project run on multiple platforms for example, in which it is much harder to ensure that a change that works perfectly on the developers machine, does not in fact break the build on all other platforms. BuildBot helps ensure that such breakage can be caught and dealt with early.

### Notifying Users ###

Of course, for BuildBot to be effective, it must communicate any errors to developers, and includes a number of different ways of doing this. Notification can be done through a web based interface, IRC, a GTK application, and/or email. For my own personal use at least, none of these were ideal. All of these notification methods interfere in some way in my development, as most of them require me to poll the application in which the notifications are posted, be that my web-browser, email or IRC client. A status delivery method which I did not have to poll is what I wanted.

### Enter BuildGrowler ###

[Growl](http://growl.info/) is an insanely useful notification service for OS X (my development platform of choice) through which any application can post messages. As far as I can tell, an ideal vehicle for posting BuildBot notifications which do not require me to constantly switch from my development environment (ie VIM in a terminal) to some other application to check if my builds have failed. Instead I get non obtrusive notifications, which I can customize to my hearts content using Growl. BuildGrowler provides this bridge between BuildBot and the Growl notification system, by enabling developers to connect to a BuildBot server and have its notifications posted as Growl notifications on their desktop. A lot less hassle then reloading a web page, checking your email, or IRC client.



