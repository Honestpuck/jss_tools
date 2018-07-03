## jss_tools

#### jss_tools - A collection of routines to convert JSS XML into python variables

This is a collection of small tool routines to make working with the data returned by python-jss easier.

At their core they turn the XML from the JSS into python dictionaries or arrays of dictionaries with the XML stringas converted into python types where possible.

Most of the functions have a matching array of keys that are used. These can can be discovered as _<function name>_keys.

There are also a few other useful routines.

Latest version can be found at https://github.com/Honestpuck/jss_tools

You will neeed python-jss working. Details at https://github.com/sheagcraig/python-jss

### A Note On Extension Attributes

JAMF do not support an extension attribute boolean type. A boolean type is so useful in programming that I fake it. If you have an EA of type 'String' that contains 'True', 'False', '1' or '0' I convert it to a boolean and convert it back if required. I don't check the type 'Number' for 0 or 1 for obvious reasons.

## Functions

#### Convert(val, typ)
Takes a string value from JSS converts it type 'typ''. `typ` is one of:
 - 'BOOL', Boolean
 - 'DATE', Date
 - 'DUTC', Date with UTC timezone information
 - 'EPOK', Unix epoch
 - 'INTN', Integer
 - 'TIME', Date and time
 - 'EBOL', A boolean extension attribute stored in a string 'True' or 'False'
 - 'ENBL', A boolean extension attribute stored in a string '1' or '0'

The date routines and TIME return a datetime object.

NOTE: The conversions DATE, DUTC and TIME use the parser routine from dateutils so they can accept a wide variety of formats, not just the one used in the JSS so you may find it easier to run convert on such as '10 Dec 2017 10:30AM' rather than build your own datetime object for comparison purposes. That's one reason for exposing it.

#### Convert_back(val, typ)
The reverse of convert. Takes a python variable and converts it to a string ready for the JSS.

####     Jopen(pref=None, pword=None)
Open a connection to the JSS. Asks for your password, returns connector. If you want to enter the URL and user pass it pref='True'. If you are running non-interactive pass it pword='password'

#### Now()
right now in datetime format.

The sole purpose of this function is to remove the need to import 'datetime' in your code and remember that it is `datetime.datetime.now()` just so we can get right now for comparison purposes.

### Functions for the `computer` record

I have split the `computer` record into 7 different functions to make it easier to handle rather than a deeper structure.

#### c_apps(computer, ignore=None)
Returns a dictionary of the apps installed. Key is name and value is version. It ignores the Apple apps (apart from Safari) or the apps listed in the optional paramater 'ignore', which is an array of app names to ignore. It also removes the `.app` at the end of the file name since  an app has it but people don't usually see it :)

#### c_attributes(computer)
Returns a dictionary of the computer's extension attributes. Key is the attribute name. The dictionary value is a dictionary with keys 'value' and 'type'.

#### c_attributes_write(attribs, computer)
Writes out any changed extension attributes to the JSS. Pass it the attribute dictionary with changed attributes and object returned from jss.Computer()

#### c_certificates(computer)
Returns an array containing a dictionary for each certificate on the computer.

Keys are:
 - common   - common name
 - identity - identity
 - utc      - expiry in UTC time
 - epoch    - expiry as seconds since Epoch
 - name     - name

#### c_groups(computer)
Returns an array of strings with the computer groups the computer belongs to

#### c_info(computer)
Returns a a dictionary of general information about the computer.

Keys are:
 - id - JSS id
 - machine_name
 - mac - Primary MAC address
 - mac2 - Secondary MAC address
 - ip
 - serial
 - barcode1
 - barcode2
 - tag
 - managed - Is it managed
 - mdm - Is it MDM capable
 - last - last enroled date
 - initial - inital enrol date
 - model - model string (i.e MacBook Late 2016)
 - model_id - model ID (i.e MacBook 2,1)
 - os - The OS version
 - os_build - The OS build number
 - master_set - Is master password set
 - AD - Active directory status
 - recovery - Is institutional recovery key set
 - user
 - name
 - email
 - building
 - room
 - profiles_count

#### c_info_write(info, computer)
Writes out any changed computer info. Pass it the info dictionary with changed info and the object returned from jss.Computer(id)

#### c_profiles(computer)
Returns an array containing a dictionary for each configuration profile on the computer.

Keys are:
 - id
 - name
 - uuid
 - is_removable

#### c_users(computer)
Returns an array containing a dictionary for each user on the computer. It ignores those whose name begins with '_'.

Keys are:
 - name
 - realname
 - uid
 - home
 - home_size_mb
 - administrator
 - file_vault_enabled

### Other JSS record types

#### category(category)
Returns a dictionary of info about a category.

#### computergroup(group)
Returns a dictionary of info about a computergroup. The key 'criteria' contains an array of dictionaries with the group membership criteria and the key 'computers' contains the same for the computers that are members of the group.

Keys are:
 - id
 - name
 - smart - If it's smart group
 - site_id
 - site_name
 - crit_count - number of criteria
 - computers_count
 - criteria - dictionary containing all the criteria
 - computers - dictionary of the computers in the group

For criteria the keys are:
 - name
 - priority
 - and_or
 - search_type
 - value

For computers the keys are:
 - id
 - name
 - mac_address
 - alt_mac_address - The second MAC address
 - serial

#### package(package)
Returns a dictionary of info about a package.

Keys are:
 - id
 - name
 - category
 - filename
 - info
 - notes
 - priority
 - reboot
 - fut - fill user template
 - feu - fill eisting users
 - boot - boot volume required
 - uninstall - allow uninstall
 - os_req
 - proc_req
 - switch - switch with package
 - install - install if reported available
 - reinstall - reinstall option
 - triggering - triggering files
 - send - send notificaitons


#### policy(policy)
Returns a dictionary of info about a policy. The key 'paks' is an array of dictionaries with info on the packages included in the policy and the key 'scripts' does the same for scripts.

Keys are:
 - id
 - name
 - enabled
 - trigger
 - checkin - trigger on checkin
 - enrollment - trigger on enrollment
 - login - trigger on login
 - logout - trigger on logout
 - network - trigger on network state change
 - startup - trigger on startup
 - other - trigger on other
 - frequency
 - cat_id - category ID
 - cat_name - category name
 - site_id
 - site_name
 - self_service - use for Self Service
 - pak_count - count of the packages included
 - script_count - count of the scripts included
 - paks - dictionary of the packages
 - scripts - dictionary of the scripts


#### script(script)
Returns a dictionary of info about a script.



_