### JSS_tools

This is a collection of small tool routines to make working with the data returned by python-jss easier.

At their core they turn the XML from the JSS into python data structures. It also converts the strings returned to valid python types where possible.

Included are a small number of utility routines, most notably `convert` to convert strings to python data types, `Jopen` to open up a connection to the JSS, `c_attributes_write` to write changed extension attributes in a computer record back to the JSS.

*This is currently under development. At the moment it is working
and passing all tests.* The master branch should be working, the other branches may not be.

For details on the functions `pydoc ./jss_tools.py` will get you the
documentation.

The directory `XML` is there for me to collect examples of the XML returned
by each function in python-jss. You can safely ignore it but I thought you may as well have it.

#### Design decisions

When working with the JSS the most expensive part of the operation is always the query to the JSS. This is why none of these routines actually perform the query. I leave the decision about when to do it to you.

At the moment there are some data structures that are arrays of dictionaries. I'd appreciate feedback on perhaps changing this to dictionaries of dictionaries with `id` or `name` as key for the outer dictionary.

If there is a python-jss call not covered that you would like then please reach out. My JSS is not well populated for some things so I have no need for some and no data to test but I can get around that if you can supply the XML returned by your JSS (sanitised, of course).

#### examples.py

A tiny file with an example of the old style and new style. For more examples look in `test.py`.

### compliance.py

Real world example. Somebody wanted a list of Macs not running the right OS
and build so I gave them the output of this.

#### test.py

My code to test the script.

