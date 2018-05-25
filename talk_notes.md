###

Good morning,

This morning I'm going to talk about using python-jss to talk to your JSS and how to wrangle the XML to get your data out.

Who here likes working with XML?

Who here thinks the XML returned frrom the JSS is perfectly formed?

How about if I tell you that the XML from one computer record is about 2500 lines of XML and there isn't a parser on the planet than can parse it properly since it's broken.

I'm not going to fault JAMF. Do you think that the JSS API is on the top of JAMF's list of concerns? No, of course not.

Actually, let's **not** talk about using python-jss. Let's  not talk about XML. It's ugly, it's boring and nobody really wants to deal with it.

python-jss
    - Hard to wrangle XML
    - Hard to remember XML
    - Ugly code

Let's talk about a better way. Hpw about a way of dealing with the data from the JSS as python arrays and dictionaries?

Let's talk about a new module I've writtien called jss_tools that takes that ugly, broken XML and turns it into python arrays and dictionaries.

    python data
    easy to write code
    cleaner code

Here's what you had to deal with using the old way. Now it's not *really* appaling. Luckily the objects python-jss returns are sub-classed from ElemenTree which is pretty good at extracting data from XML and deals with malformed XML quite well. But the code isn't elegant and you have to wade through a bunch of XML to figure out exactly what those strings need to be.

Here's exactly the same thing written using jss_tools. Not only does it look a little cleaner, it's much easier to write.

How about a little demo?




