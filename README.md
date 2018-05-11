### JSS_tools

This is a collection of small tool routines to make working with the data returned by python-jss easier.

At their core they turn the XML from the JSS into python data structures. It also converts the strings retuened to valid python types where possible.

*This is currently under continual developent. At the moment it is working
and passing all tests.

`Jopen()` opens a connection to the JSS. It uses the URL and user name in the
defaults preferences but asks for your password so you don't need to have the password in a script or in the preferences. It returns the JSS instance. It basically requires python-jss to be working.

For details on the functions `pydoc ./jss_tools.py` will get you the
documentation.

#### Design decisions

When working with the JSS the most expensive part of the operation is always the query to the JSS. This is why none of these routines actually perform the query. I leave the decision about when to do it to you.

At the moment there are some data structures that are arrays of dictionaries. I'd appreciate feedback on perhaps changing this to dictionaries of dicitonaries with `id` as key for the outer dictionary.

#### examples.py

A tiny file with an example of the old style and new style. For more examples look in `test.py`.

#### test.py

My code to test the script.

