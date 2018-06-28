### JSS_tools

This is a collection of small tool routines to make working with the data returned by python-jss easier.

At their core they turn the XML from the JSS into python data structures. It also converts the strings returned to valid python types where possible.

Included are a small number of utility routines, most notably `convert` to convert strings to python data types, `Jopen` to open up a connection to the JSS, `c_attributes_write` to write changed extension attributes in a computer record back to the JSS and `c_info_write` to write changed computer info back to the JSS.

*This is currently under development. At the moment it is working
and passing all tests.* The master branch is working, the other branches may not be.

For details on the functions `pydoc ./jss_tools.py` will get you the
documentation.

#### Design decisions

When working with the JSS the most expensive part of the operation is always the query to the JSS. This is why none of these routines actually perform the query. I leave the decision about when to do it to you.

I'm open to any feedback about the structures returned. If you think they could be improved I'm open to suggestions.

If there is an API call not covered that you would like then please reach out. My JSS is not well populated for some things so I have no need for some and no data to test but I can get around that if you can supply the XML returned by your JSS (sanitised, of course, to remove any personal or corporate info).

## A Note On Extension Attributes

JAMF do not support an extension attribute boolean type. A boolean type is so
useful in programming that I fake it. If you have an EA of type 'String' that
contains 'True', 'False', '1' or '0' I convert it to a boolean and convert it
back if required. I don't check the type 'Number' for 0 or 1 for obvious
reasons.

#### examples.py

A tiny file with an example of the new style.

### compliance.py

Real world example. Somebody wanted a list of Macs not running the right OS
and build so I gave them the output of this.

#### test.py

My code to test the script. It's not really comprehensive but it does the job.

### Notes

I'm reaching out for any users who can provide feedback. Seriously, criticisms and suggestions happily accepted.

Better documentation is in the works. I will also be providing more examples of what can be easily done in Python with `jss_tools`





