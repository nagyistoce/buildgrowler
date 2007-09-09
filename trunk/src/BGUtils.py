import objc
objc.loadBundle("BGUtils", globals(),
     bundle_path=objc.pathForFramework(u'@executable_path@/../../Frameworks/BGUtils.framework'))
del objc

def fourCharCode2Int(s):
    # This really only works on strings of length 4
    assert type(s) == str
    assert len(s) == 4
    i = 0
    # perhaps I should not be so lazy and just write this out :)
    for c in s:
        i = (i << 8) + ord(c)
    print i
    return i 
