## Setting up your BuildBot Server ##

BuildGrowler uses the PBListener status service in BuildBot, which must be enabled on the BuildBot servers that you are going to connect to. If you do not administer a the BuildBot servers yourself, you may have to contact the administrator and  ask them to enable the PBListener status service.

### Enabling PBListener ###

> The BuildBot documentation contains instructions for [setting up a PBListener](http://buildbot.net/repos/release/docs/buildbot.html#PBListener). For your convenience the relevant code snippet is replicated here.

```
     import buildbot.status.client
     pbl = buildbot.status.client.PBListener(port=int, user=str, passwd=str)
     c['status'].append(pbl)
```

You should probably add this bit of code around your other status services. You should always specify a port, user, and password, or you may be surprised by the default values (which for user and password is **not** blank, as of BuildBot 0.7.5)



