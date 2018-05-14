### JSS_tools

This is a collection of small tool routines to make working with the data returned by python-jss easier.

At their core they turn the XML from the JSS into python data structures. It also converts the strings returned to valid python types where possible.

*This is currently under continual developent. At the moment it is working
and passing all tests.*

For details on the functions `pydoc ./jss_tools.py` will get you the
documentation.

The directory `XML` is there for me to collect examples of the XML returned
by each function in python-jss. You can safely ignore it but I thought you may as well have it.

#### Design decisions

When working with the JSS the most expensive part of the operation is always the query to the JSS. This is why none of these routines actually perform the query. I leave the decision about when to do it to you.

At the moment there are some data structures that are arrays of dictionaries. I'd appreciate feedback on perhaps changing this to dictionaries of dictionaries with `id` as key for the outer dictionary.

Some functions can be optionally passed a list of keys for information to be
retrieved but since this adds some code complexity and testing has shown that
the biggest cost in time by far for using JSS data is the API request even
on large record types like a computer record I'm considering removing this.
Use cases for leaving it would be appreciated.

If there is a python-jss call not covered that you would like then please reach out. My JSS is not well populated for some things so I have no need for some and no data to test but I can get around that if you can supply the XML returned by your JSS (sanitised, of course).

Feedback to honestpuck@gmail.com

#### examples.py

A tiny file with an example of the old style and new style. For more examples look in `test.py`.

### compliance.py

Real world example. Somebody wanted a list of Macs not running the right OS
and build so I gave them the output of this.

#### test.py

My code to test the script.

