### JSS_tools

This is a collection of small tool routines to make working with the data returned by python-jss.

At their core they turn the XML from the JSS into python data structures.

`info(record, keys)` is passed a computer record and returns a dictionary of general information about the computer. It has a default list of information it returns but you can optionally pass it your own.

`apps(computer, ignore)` returns a dictionary of
the apps installed. Key is the name and value is version. It ignores the Apple apps or the apps listed in the optional paramater 'ignore',

`attributes(computer)` returns a dictionary of the computers extension attributes. Each is added twice so you can get the value by the attribute name or id. Only gives you the value, not the type.

`groups(computer)` returns an array of the groups the computer is a member of.

`package(pak, keys)` returns a dictionary of info about a package.

`policy(policy, keys)` returns a dictionary of info about a policy. The key 'paks' is an array of dictionaries with info on the packages included in the policy and the key 'scripts' does the same for scripts.




