#
# jss_tools.py
#
# functions to turn JSS records into more useful
# python variables, mostly dictionaries and arrays.
#
# Tony Williams
#
"""A collection of routines to convert JSS XML into python variables

This is a collection of small tool routines to make working with
the data returned by python-jss easier.

At their core they turn the XML from the JSS into python dictionaries or
arrays of dictionaries with the XML stringas converted into python types
where possible.

Most of the functions have a matching array of keys that are used. These can
can be discovered as _<function name>_keys.

There are also a few other useful routines.

Latest version can be found at https://github.com/Honestpuck/jss_tools

You will neeed python-jss working. Details at
https://github.com/sheagcraig/python-jss
"""

__author__ = "Tony Williams"
__version__ = 1.2
__date__ = '28 May 2018'

import jss
import getpass
from dateutil import parser
import datetime
import time
import copy


# some low level useful routines
def Convert(val, typ):
    """Takes a string value from JSS converts it type 'typ''.
    `typ` is one of:
    'BOOL', Boolean
    'DATE', Date
    'DUTC', Date with UTC timezone information
    'EPOK', Unix epoch
    'INTN', Integer
    'TIME'. Date and time

    The date routines and TIME return a datetime object.

    NOTE: The conversions DATE, DUTC and TIME use the parser routine from
    dateutils so they can accept a wide variety of formats, not just the one
    used in the JSS so you may find it easier to run convert on such as
    '10 Dec 2017 10:30AM' rather than build your own datetime object for
    comparison purposes. That's one reason for exposing it.
    """
    return {
        'BOOL': lambda x: x == 'true',
        'INTN': lambda x: int(x),
        'DATE': lambda x: parser.parse(x),
        'DUTC': lambda x: dateutil.parser.parse(x),
        'EPOK': lambda x: datetime.datetime.fromtimestamp(int(x)/1000),
        'TIME': lambda x: parser.parse(x),
        'STRG': lambda x: x,
    }[typ](val)


def Convert_back(val, typ):
    """The reverse of convert. Takes a python variable and converts it to a
    string ready for the JSS.
    """
    return {
        'BOOL': lambda x: str(x).lower(),
        'INTN': lambda x: str(x),
        'DATE': lambda x: str(x),
        'DUTC': lambda x: str(x),
        'EPOK': lambda x: time.mktime(x.timetuple()) * 1000,
        'TIME': lambda x: str(x),
        'STRG': lambda x: x,
    }[typ](val)


def Now():
    '''right now in datetime format.

    The sole purpose of this function is to remove the need to import
    'datetime' in your code and remember that it is `datetime.datetime.now()`
    just so we can get right now for comparison purposes. Yes, OK, I'm lazy.
    '''
    return datetime.datetime.now()


def Jopen(pref=None):
    """Open a connection to the JSS. Asks for your password,
    returns connector. If you want to enter the URL and user
    pass it 'True'.
    """
    jss_prefs = jss.JSSPrefs()
    if pref:
        jss_prefs.url = raw_input("URL: ")
        jss_prefs.user = raw_input("User: ")
    jss_prefs.password = getpass.getpass()
    return jss.JSS(jss_prefs)


# Routines for the computer record

_c_info_keys = [
    # general
    ['general/id', 'id'],
    ['general/name', 'machine_name'],
    ['general/mac_address', 'mac'],
    ['general/alt_mac_address', 'mac2'],
    ['general/ip_address', 'ip'],
    ['general/serial_number', 'serial'],
    ['general/barcode_1', 'barcode1'],
    ['general/barcode_2', 'barcode2'],
    ['general/asset_tag', 'tag'],
    ['general/remote_management/managed', 'managed'],
    ['general/mdm_capable', 'mdm'],
    ['general/last_contact_time', 'last'],
    ['general/initial_entry_date', 'initial'],
    ['hardware/model', 'model'],
    ['hardware/model_identifier', 'model_id'],
    ['hardware/os_version', 'os'],
    ['hardware/os_build', 'os_build'],
    ['hardware/master_password_set', 'master_set'],
    ['hardware/active_directory_status', 'AD'],
    ['hardware/institutional_recovery_key', 'recovery'],
    # user
    ['location/username', 'user'],
    ['location/real_name', 'name'],
    ['location/email_address', 'email'],
    ['location/building', 'building'],
    ['location/room', 'room'],
    # purchasing
    # ['purchasing/is_purchased', 'purchased'],
    # ['purchasing/is_leased', 'leased'],
    # ['purchasing/po_number', 'po_num'],
    # ['purchasing/vendor', 'vendor'],
    # ['purchasing/applecare_id', 'applecare_id'],
    # ['purchasing/purchase_price', 'price'],
    # ['purchasing/purchasing_account', 'pur_account'],
    # ['purchasing/po_date', 'po_date'],
    # ['purchasing/warranty_expires', 'warranty_epires'],
    # ['purchasing/lease_expires', 'lease_expires'],
    # ['purchasing/purchasing_contact', 'pur_contact'],
    # ['purchasing/os_applecare_id', 'applecare'],
    # ['purchasing/os_maintenance_expires', 'maintenance_expires'],
    ['configuration_profiles/size', 'profiles_count']
]

_c_info_convert_keys = [
    ['initial', 'DATE'],
    ['last', 'TIME'],
    ['managed', 'BOOL'],
    ['master_set', 'BOOL'],
    ['mdm_capable', 'BOOL'],
    ['profiles_count', 'INTN']
]


def c_info(computer):
    """Returns a a dictionary of general information about the computer.
    """
    dict = {}
    for key in _c_info_keys:
        dict.update({key[1]: computer.findtext(key[0])})
    for cc in _c_info_convert_keys:
        dict[cc[0]] = Convert(dict[cc[0]], cc[1])
    return dict


def c_info_write(info, computer):
    """Writes out any changed computer info. Pass it the info
    dictionary with changed info and the object returned from jss.Computer()
    """
    our_info = copy.deepcopy(info)
    for key in _c_info_convert_keys:
        our_info[key[0]] = Convert_back(our_info[key[0]], key[1])
    for key in _c_info_keys:
        computer.find(key[0]).text = our_info[key[1]]
    computer.save()


# apps to ignore in app list (Apple apps)
_c_apps_ignore = [
    # Standard Apple apps
    'Activity Monitor',
    'AirPort Utility',
    'App Store',
    'Audio MIDI Setup',
    'Automator',
    'Boot Camp Assistant',
    'Bluetooth File Exchange',
    'Calculator',
    'Calendar',
    'Chess',
    'ColorSync Utility',
    'Console',
    'Contacts',
    'Dashboard',
    'Dictionary',
    'Digital Color Meter',
    'Disk Utility',
    'DVD Player',
    'FaceTime',
    'Font Book',
    'Grab',
    'Grapher',
    'iBooks',
    'Image Capture',
    'iTunes',
    'Keychain Access',
    'Launchpad',
    'Mail',
    'Maps',
    'Messages',
    'Migration Assistant',
    'Mission Control',
    'Notes',
    'Photo Booth',
    'Photos',
    'Preview',
    'QuickTime Player',
    'Reminders',
    'Safari',
    'Script Editor',
    'Siri',
    'Stickies',
    'System Information',
    'System Preferences',
    'Terminal',
    'TextEdit',
    'Time Machine',
    'VoiceOver Utility',
    # JAMF
    # 'Self Service',
    # MS
    # 'Microsoft Excel',
    # 'Microsoft OneNote',
    # 'Microsoft Outlook',
    # 'Microsoft PowerPoint',
    # 'Microsoft Teams',
    # 'Microsoft Word',
    # 'OneDrive',
    # 'Skype for Business',
]


def c_apps(computer, ignore=None):
    """Returns a dictionary of the apps installed. Key is name and value is
    version. It ignores the Apple apps or the apps listed in the optional
    paramater 'ignore', which is an array of app names to ignore. It also
    removeds the `.app` at the end of the file name since  an app has it
    but people don't usually see it :)
    """
    if not ignore:
        ignore = _c_apps_ignore
    dict = {}
    for app in computer.findall('software/applications/application'):
        nm = app.findtext('name').split('.')[0]
        if nm not in ignore:
            dict.update({nm: app.findtext('version')})
    return dict


def c_attributes(computer):
    """Returns a dictionary of the computer's extension attributes. Key is
    the attribute name.The dictionary value is a dictionary with keys 'value'
    and 'type'.
    """
    dict = {}
    for attr in computer.findall('extension_attributes/extension_attribute'):
        nm = attr.findtext('name')
        ty = attr.findtext('type')
        vl = Convert(attr.findtext('value', ty))
        dict.update({nm: {'value': vl, 'type': ty)})
    return dict


def c_attributes_write(attribs, computer):
    """Writes out any changed extension attributes. Pass it the attribute
    dictionary with changed attributes and object returned from jss.Computer()
    """
    for attr in computer.findall('extension_attributes/extension_attribute'):
        nm = attr.findtext('name')
        val = attr.findtext('value')
        if attribs[nm]['value'] != val:
            new_val = Convert_back(attribs[nm]['value'], attribs[nm]['type'])
            attr.find('value').text = new_val
    computer.save()


def c_groups(computer):
    """ Returns an array of the computer groups the computer belongs to.
    """
    ar = []
    for group in computer.find('groups_accounts/computer_group_memberships'):
        ar.append(group.text)
    return ar


_c_user_keys = [
    'name',
    'realname',
    'uid',
    'home',
    'home_size_mb',
    'administrator',
    'file_vault_enabled',
]

_c_user_convert_keys = [
    ['administrator', 'BOOL'],
    ['file_vault_enabled', 'BOOL'],
]


def c_users(computer):
    """Returns an array containing a dictionary for each user on the
    computer. It ignores those whose name begins with '_'.
    """
    ar = []
    for u in computer.find('groups_accounts/local_accounts'):
        if u.findtext('name')[0] is not '_':
            dict = {}
            for key in _c_user_keys:
                dict.update({key: u.findtext(key)})
            for cc in _c_user_convert_keys:
                dict[cc[0]] = Convert(dict[cc[0]], cc[1])
            ar.append(dict)
    return ar


_c_certificates_keys = [
    ['common_name', 'common'],
    ['identity', 'identity'],
    ['expires_utc', 'utc'],
    ['expires_epoch', 'epoch'],
    ['name', 'name'],
]

_c_certificates_convert_keys = [
    ['utc', 'DUTC'],
    ['epoch', 'EPOK'],
]


def c_certificates(computer):
    """Returns an array containing a dictionary for each certificate on
    the computer.
    """
    ar = []
    for cert in computer.findall('certificates/certificate'):
        dict = {}
        for key in _c_certificates_keys:
            dict.update({key[1]: cert.findtext(key[0])})
        for cc in _c_certificates_convert_keys:
            dict[cc[0]] = Convert(dict[cc[0]], cc[1])
        ar.append(dict)
    return ar


_c_profiles_keys = [
    'id',
    'name',
    'uuid',
    'is_removable'
]

_c_profiles_convert_keys = [
    ['is_removable', 'BOOL'],
]


def c_profiles(computer):
    """Returns an array containing a dictionary for each configuration
    profile on the computer.
    """
    ar = []
    for profile in computer.findall(
            'configuration_profiles/configuration_profile'):
        dict = {}
        for key in _c_profiles_keys:
            dict.update({key: profile.findtext(key)})
        for cc in _c_profiles_convert_keys:
            dict[cc[0]] = Convert(dict[cc[0]], cc[1])
        ar.append(dict)
    return ar


# Other record types

_packages_keys = [
    ['id', 'id'],
    ['name', 'name'],
    ['category', 'category'],
    ['filename', 'filename'],
    ['info', 'info'],
    ['notes', 'notes'],
    ['priority', 'priority'],
    ['reboot_required', 'reboot'],
    ['fill_user_template', 'fill_user'],
    ['fill_existing_users', 'fill'],
    ['boot_volume_required', 'boot_req'],
    ['allow_uninstalled', 'allow_uninst'],
    ['os_requirements', 'os_req'],
    ['required_processor', 'req_proc'],
    ['switch_with_package', 'switch_with_pak'],
    ['install_if_reported_available', 'install_if_avail'],
    ['reinstall_option', 'reinstall'],
    ['triggering_files', 'triggering'],
    ['send_notification', 'send_not'],
]

_packages_convert_keys = [
    ['reboot', 'BOOL'],
    ['fill_user', 'BOOL'],
    ['fill', 'BOOL'],
    ['boot_req', 'BOOL'],
    ['allow_uninst', 'BOOL'],
    ['install_if_avail', 'BOOL'],
    ['send_not', 'BOOL'],
]


def package(package):
    """Returns a dictionary of info about a package.
    """
    dict = {}
    for key in _packages_keys:
        dict.update({key[1]: package.findtext(key[0])})
    for cc in _packages_convert_keys:
        dict[cc[0]] = Convert(dict[cc[0]], cc[1])
    return dict


_pol_keys = [
    ['general/id', 'id'],
    ['general/name', 'name'],
    ['general/enabled', 'enabled'],
    ['general/trigger', 'trigger'],
    ['general/trigger_checkin', 'checkin'],
    ['general/trigger_enrollment_complete', 'enrollment'],
    ['general/trigger_login', 'login'],
    ['general/trigger_logout', 'logout'],
    ['general/trigger_network_state_change', 'network'],
    ['general/trigger_startup', 'startup'],
    ['general/trigger_other', 'other'],
    ['general/frequency', 'frequency'],
    ['general/category/id', 'cat_id'],
    ['general/category/name', 'cat_name'],
    ['general/site/id', 'site_id'],
    ['general/site/name', 'site_name'],
    ['self_service/use_for_self_service', 'self_service'],
    ['package_configuration/packages/size', 'pak_count'],
    ['scripts/size', 'script_count'],
]

_pol_pak_keys = [
    'id',
    'name',
    'action',
    'fut',
    'feu',
    'autorun',
]

_pol_script_keys = [
    'id',
    'name',
    'priority',
    'parameter4',
    'parameter5',
    'parameter6',
    'parameter7',
    'parameter8',
    'parameter9',
    'parameter10',
    'parameter11',
]

_pol_convert_keys = [
    ['checkin', 'BOOL'],
    ['enabled', 'BOOL'],
    ['enrollment', 'BOOL'],
    ['login', 'BOOL'],
    ['logout', 'BOOL'],
    ['self_service', 'BOOL'],
    ['startup', 'BOOL'],
]

_pol_pak_convert_keys = [
    ['fut', 'BOOL'],
    ['feu', 'BOOL'],
]


def policy(policy):
    """Returns a dictionary of info about a policy. The key 'paks' is an
    array of dictionaries with info on the packages included in the policy
    and the key 'scripts' does the same for scripts.
    """
    dict = {}
    for key in _pol_keys:
        dict.update({key[1]: policy.findtext(key[0])})
    for cc in _pol_convert_keys:
        dict[cc[0]] = Convert(dict[cc[0]], cc[1])

    paks = []
    if dict['pak_count'] == '0':
        paks = [None]
    else:
        for pak in policy.findall('package_configuration/packages/package'):
            this_pak = {}
            for pak_key in _pol_pak_keys:
                this_pak.update({pak_key: pak.findtext(pak_key)})
            for cc in _pol_pak_convert_keys:
                this_pak[cc[0]] = Convert(this_pak[cc[0]], cc[1])
            paks.append(this_pak)
    dict.update({'paks': paks})

    scripts = []
    if dict['script_count'] == '0':
        scripts = [None]
    else:
        for script in policy.findall('scripts/script'):
            this_script = {}
            for s_key in _pol_script_keys:
                this_script.update({s_key: script.findtext(s_key)})
            scripts.append(this_script)
    dict.update({'scripts': scripts})

    return dict


_script_keys = [
    ['id', 'id'],
    ['name', 'name'],
    ['category', 'category'],
    ['filename', 'filename'],
    ['info', 'info'],
    ['notes', 'notes'],
    ['priority', 'priority'],
    ['parameter/parameter4', 'par4'],
    ['parameter/parameter5', 'par5'],
    ['parameter/parameter6', 'par6'],
    ['script_contents', 'contents'],
]


def script(script):
    """Returns a dictionary of info about a script.
    """
    dict = {}
    for key in _script_keys:
        dict.update({key[1]: script.findtext(key[0])})
    return dict


_computergroup_keys = [
    ['id', 'id'],
    ['name', 'name'],
    ['is_smart', 'smart'],
    ['site/id', 'site_id'],
    ['site/name', 'site_name'],
    ['criteria/size', 'crit_count'],
    ['computers/size', 'computers_count'],
]

_computergroup_criteria_keys = [
    'name',
    'priority',
    'and_or',
    'search_type',
    'value',
]

_computergroup_computer_keys = [
    'id',
    'name',
    'mac_address',
    'alt_mac_address',
    'serial',
]


def computergroup(group):
    """Returns a dictionary of info about a computergroup. The key 'criteria'
    contains an array of dictionaries with the group membership criteria and
    the key 'computers' contains the same for the computers that are members
    of the group.
    """
    dict = {}
    for key in _computergroup_keys:
        dict.update({key[1]: group.findtext(key[0])})
    dict['smart'] = Convert(dict['smart'], 'BOOL')

    criteria = []
    if dict['crit_count'] == 0:
        criteria = [None]
    else:
        for criterion in group.findall('criteria/criterion'):
            this_crit = {}
            for cr_key in _computergroup_criteria_keys:
                this_crit.update({cr_key: criterion.findtext(cr_key)})
            criteria.append(this_crit)
    dict.update({'criteria': criteria})

    computers = []
    if dict['computers_count'] == 0:
        computers = [None]
    else:
        for computer in group.findall('computers/computer'):
            this_comp = {}
            for cm_key in _computergroup_computer_keys:
                this_comp.update({cm_key: computer.findtext(cm_key)})
            computers.append(this_comp)
    dict.update({'computers': computers})

    return dict


_category_keys = [
    'id',
    'name',
    'priority',
]


def category(category):
    """Returns a dictionary of info about a category.
    """
    dict = {}
    for key in _category_keys:
        dict.update({key: category.findtext(key)})
    dict['priority'] = Convert(dict['priority'], 'INTN')
    return dict
