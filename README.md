### JSS_tools

This is a collection of small tool routines to make working with the data returned by python-jss easier.

At their core they turn the XML from the JSS into python data structures.

**This is currently under heavy development and shouldn't be used for anything but testing of itself. At the moment the `master` branch is working and passing
`Jopen()` opens a connection to the JSS. It uses the URL and user name in the
defaults preferences but asks for your password so you don't need to have the password in a script or in the preferences. It returns the JSS instance. It basically requires python-jss to be working.

#### Information from a computer record

`c_info(computer, keys)` is passed a computer record and returns a dictionary of general information about the computer. It has a default list of information it returns but you can optionally pass it your own.

`c_apps(computer, ignore)` returns a dictionary of
the apps installed. Key is the name and the value is the version. It ignores the Apple apps or the apps listed in the optional paramater 'ignore' (an array of the names).

`c_attributes(computer)` returns a dictionary of the computer's extension attributes. Each is added twice so you can get the value by the attribute name or id. Only gives you the value, not the type.

`c_groups(computer)` returns an array of the groups the computer is a member of.

`c_users(computer)` returns an array containing a dictionary for each user on the computer. It ignores those whose name begins with '_'.

`c_certificates(computer)` returns an array containing a dictionary for each cetificate on the computer.

`c_profiles(computer)` returns an array containing a dictionary for each configuration profile on the computer.

#### Other JSS records

`package(pak, keys)` returns a dictionary of info about a package.

`policy(policy, keys)` returns a dictionary of info about a policy. The key `'paks'` is an array of dictionaries with info on the packages included in the policy and the key `'scripts'` does the same for scripts.

`script(script, keys)` returns a dictionary of info about a script.

#### Design decisions

When working with the JSS the most expensive part of the operation is always the query to the JSS. This is why none of these routines actually perform the query. I leave the decision about when to do it to you.

At the moment there are some data structures that are arrays of dictionaries. I'd appreciate feedback on perhaps changing this to dictionaries of dicitonaries with `id` as key for the outer dictionary.

#### examples.py

A tiny file with an example of the old style and new style. For more examples look in `test.py`.

#### tools_convert.py

I've started working on some routines to take the string data and convert _that_ to python types. This is extremely limited at the moment, it's basically a proof of concept for later work.







