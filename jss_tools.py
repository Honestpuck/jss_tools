#
# JSS_tools.py
#
# functions to turn a JSS records into more useful
# python variables, mostly dictionaries and arrays.
#
# Tony Williams (ARW)
#
# 10 May 2018
#
"""A collection of routines to convert JSS XML into python variables

This is a collection of small tool routines to make working with
the data returned by python-jss easier.

At their core they turn the XML from the JSS into python dictionaries or
arrays of dictionaries with the XML stringas converted into python types
where possible.

Each of the functions has a matching array of keys that are used. These can
can be discovered as _<function name>_keys.

Latest version can be found at https://github.com/Honestpuck/jss_tools

You will neeed python-jss working. Details at
https://github.com/sheagcraig/python-jss
"""

__author__ = "Tony Williams"
__version__ = 0.4
__date__ = '11 May 2018'

# required for jss
import jss
import getpass

# for string to data conversion
from dateutil import parser
from datetime import datetime


# some low level useful routines
def convert(val, typ):
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
    '10 Dec 2108' rather than build your own datetime object for comparison
    purposes. That's why I expose it to you.
    """
    return {
        'BOOL': lambda x: x == 'true',
        'INTN': lambda x: int(x),
        'DATE': lambda x: parser.parse(x),
        'DUTC': lambda x: parser.parse(x),
        'EPOK': lambda x: datetime.fromtimestamp(int(x)/1000),
        'TIME': lambda x: parser.parse(x),
    }[typ](val)


def now():
    '''right now in datetime format.

    The sole purpose of this function is to remove the need to import
    'datetime' in your code and remember that it is `datetime.datetime.now()`
    just so we can get right now for comparison purposes.
    '''
    return datetime.now()


def Jopen():
    """Open a connection to the JSS. Asks for your password,
    returns connector
    """
    jss_prefs = jss.JSSPrefs()
    jss_prefs.password = getpass.getpass()
    return jss.JSS(jss_prefs)


# Routines for the computer record

_c_info_keys = [
    # general
    ['general/id', 'id'],
    ['general/name', 'name'],
    ['general/mac_address', 'mac'],
    ['general/alt_mac_address', 'mac2'],
    ['general/ip_address', 'ip'],
    ['general/serial_number', 'serial'],
    ['general/barcode_1', 'bar1'],
    ['general/barcode_2', 'bar2'],
    ['general/asset_tag', 'tag'],
    ['general/remote_management/managed', 'managed'],
    ['general/mdm_capable', 'mdm'],
    ['general/last_contact_time', 'last'],
    ['general/initial_entry_date', 'initial'],
    ['hardware/model', 'model'],
    ['hardware/model_identifier', 'model_id'],
    ['hardware/os_version', 'os'],
    ['hardware/os_build', 'os_build'],
    ['hardware/master_password_set', 'master'],
    ['hardware/active_directory_status', 'AD'],
    ['hardware/institutional_recovery_key', 'recovery'],
    # user
    ['location/username', 'user'],
    ['location/real_name', 'name'],
    ['location/email_address', 'email'],
    # purchasing
    # ['purchasing/is_purchased', 'purchased'],
    # ['purchasing/is_leased', 'leased'],
    # ['purchasing/po_number', 'po_num'],
    # ['purchasing/vendor', 'vendor'],
    # ['purchasing/applecare_id', 'applecare'],
    # ['purchasing/purchase_price', 'price'],
    # ['purchasing/purchasing_account', 'pur_account'],
    # ['purchasing/po_date', 'po_date'],
    # ['purchasing/warranty_expires', 'warranty'],
    # ['purchasing/lease_expires', 'lease'],
    # ['purchasing/purchasing_contact', 'pur_contact'],
    # ['purchasing/os_applecare_id', 'applecare'],
    # ['purchasing/os_maintenance_expires', 'maintenance'],
    ['configuration_profiles/size', 'profiles_count']
]

_c_info_convert_keys = [
    ['initial', 'DATE'],
    ['last', 'TIME'],
    ['managed', 'BOOL'],
    ['master', 'BOOL'],
    ['mdm', 'BOOL'],
    ['profiles_count', 'INTN']
]


# general information
def c_info(computer, keys=None):
    """Returns a a dictionary of general information about the computer.
    It has a default list of information it returns but you can optionally
    pass it your own.
    """
    if not keys:
        keys = _c_info_keys
    dict = {}
    for key in keys:
        dict.update({key[1]: computer.findtext(key[0])})
    for cc in _c_info_convert_keys:
        if cc[0] in dict:
            dict[cc[0]] = convert(dict[cc[0]], cc[1])
    return dict


# apps to ignore in app list (Apple apps)
_c_ignore_apps = [
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
    removeds the `.app` at the end of the file name since  by definition
    an app has it but people don't usually see it :)
    """
    if not ignore:
        ignore = _c_ignore_apps
    dict = {}
    for app in computer.findall('software/applications/application'):
        nm = app.findtext('name').split('.')[0]
        if nm not in ignore:
            dict.update({nm: app.findtext('version')})
    return dict


def c_attributes(computer):
    """Returns a dictionary of the computers extension attributes. Each is
    added twice so you can get the value by the attribute name or id. Only
    gives you the value, not the type.
    """
    dict = {}
    for attr in computer.findall('extension_attributes/extension_attribute'):
        id = attr.findtext('id')
        nm = attr.findtext('name')
        val = attr.findtext('value')
        dict.update({id: val, nm: val})
    return dict


def c_groups(computer):
    """ Returns an array of the computer groups computer belongs to.
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
                dict[cc[0]] = convert(dict[cc[0]], cc[1])
            ar.append(dict)
    return ar


_c_certificates_keys = [
    ['common_name', 'common'],
    ['identity', 'identity'],
    ['expires_utc', 'utc'],
    ['expires_epoch', 'epoch'],
    ['name', 'name'],
]


def c_certificates(computer):
    """Returns an array containing a dictionary for each cetificate on
    the computer.
    """
    ar = []
    for cert in computer.findall('certificates/certificate'):
        dict = {}
        for key in _c_certificates_keys:
            dict.update({key[1]: cert.findtext(key[0])})
        if dict['utc']:
            dict['utc'] = convert(dict['utc'], 'DUTC')
        if dict['epoch']:
            dict['epoch'] = convert(dict['epoch'], 'EPOK')
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


def c_profiles(computer, keys=None):
    """Returns an array containing a dictionary for each configuration
    profile on the computer.
    """
    if not keys:
        keys = _c_profiles_keys
    ar = []
    for profile in computer.findall(
            'configuration_profiles/configuration_profile'):
        dict = {}
        for key in _prof_keys:
            dict.update({key: profile.findtext(key)})
        for cc in _c_profiles_convert_keys:
            if cc[0] in dict:
                dict[cc[0]] = convert(dict[cc[0]], cc[1])
        ar.append(dict)
    return ar


# Other record types

_c_packages_keys = [
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

_c_packages_convert_keys = [
    ['reboot', 'BOOL'],
    ['fill_user', 'BOOL'],
    ['fill', 'BOOL'],
    ['boot_req', 'BOOL'],
    ['allow_uninst', 'BOOL'],
    ['install_if_avail', 'BOOL'],
    ['send_not', 'BOOL'],
]


def package(package, keys=None):
    """Returns a dictionary of info about a package.
    """
    if not keys:
        keys = _c_packages_keys
    dict = {}
    for key in keys:
        dict.update({key[1]: package.findtext(key[0])})
    for cc in _c_packages_convert_keys:
        if cc[0] in dict:
            dict[cc[0]] = convert(dict[cc[0]], cc[1])

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


def policy(policy, keys=None):
    """Returns a dictionary of info about a policy. The key `'paks'` is an
    array of dictionaries with info on the packages included in the policy
    and the key `'scripts'` does the same for scripts.
    """
    if not keys:
        keys = _pol_keys
    dict = {}
    for key in keys:
        value = policy.findtext(key[0])
        dict.update({key[1]: value})
    for cc in _pol_convert_keys:
        if cc[0] in dict:
            dict[cc[0]] = convert(dict[cc[0]], cc[1])
    # build list of packages in policy
    paks = []
    if dict['pak_count'] == '0':
        paks = [None]
    else:
        for pak in policy.findall('package_configuration/packages/package'):
            this_pak = {}
            for pak_key in _pol_pak_keys:
                value = pak.findtext(pak_key)
                this_pak.update({pak_key: value})
            for cc in _pol_pak_convert_keys:
                this_pak[cc[0]] = convert(this_pak[cc[0]], cc[1])
            paks.append(this_pak)
    dict.update({'paks': paks})
    # build list of scripts in policy
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


def script(script, keys=None):
    """Returns a dictionary of info about a script.
    """
    if not keys:
        keys = _script_keys
    dict = {}
    for key in keys:
        value = script.findtext(key[0])
        dict.update({key[1]: value})
    return dict


_group_keys = [
    ['id', 'id'],
    ['name', 'name'],
    ['is_smart', 'smart'],
    ['site/id', 'site_id'],
    ['site/name', 'site_name'],
    ['criteria/size', 'crit_count'],
    ['computers/size', 'computers_count'],
]

_group_criteria_keys = [
    'name',
    'priority',
    'and_or',
    'search_type',
    'value',
]

_group_computer_keys = [
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
    for key in _group_keys:
        value = group.findtext(key[0])
        dict.update({key[1]: value})
    dict['smart'] = convert(dict['smart'], 'BOOL')
    criteria = []
    if dict['crit_count'] == 0:
        criteria = [None]
    else:
        for criterion in group.findall('criteria/criterion'):
            this_crit = {}
            for c_key in _group_criteria_keys:
                this_crit.update({c_key: criterion.findtext(c_key)})
            criteria.append(this_crit)
    dict.update({'criteria': criteria})

    computers = []
    if dict['computers_count'] == 0:
        computers = [None]
    else:
        for computer in group.findall('computers/computer'):
            this_comp = {}
            for c_key in _group_computer_keys:
                this_comp.update({c_key: computer.findtext(c_key)})
            computers.append(this_crit)
    dict.update({'computers': computers})
    return dict
