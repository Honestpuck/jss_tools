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

## A Note On Extension Attributes

JAMF do not support an extension attribute boolean type. A boolean type is so
useful in programming that I fake it. If you have an EA of type 'String' that
contains 'True', 'False', '1' or '0' I convert it to a boolean and convert it
back if required. I don't check the type 'Number' for 0 or 1 for obvious
reasons.
"""

__author__ = "Tony Williams"
__version__ = 1.3
__date__ = '21 June 2018'

import jss
import getpass
from dateutil import parser
import datetime
import time
import copy
from xml.etree import ElementTree


# some low level useful routines
def Convert(val, typ):
    """Takes a string value from JSS converts it type 'typ''.
    `typ` is one of:
    'BOOL', Boolean
    'DATE', Date
    'DUTC', Date with UTC timezone information
    'EPOK', Unix epoch
    'INTN', Integer
    'TIME', Date and time
    'EBOL', A boolean extension attribute stored in a string 'True' or 'False'
    'ENBL', A boolean extension attribute stored in a string '1' or '0'

    2018-07-02T16:06:50.653+1000

    The date routines and TIME return a datetime object.

    NOTE: The conversions DATE, DUTC and TIME use the parser routine from
    dateutils so they can accept a wide variety of formats, not just the one
    used in the JSS so you may find it easier to run convert on such as
    '10 Dec 2017 10:30AM' rather than build your own datetime object for
    comparison purposes. That's one reason for exposing it.
    """
    return {
        'BOOL': lambda x: x.lower() == 'true',
        'INTN': lambda x: int(x),
        'DATE': lambda x: parser.parse(x),
        'DUTC': lambda x: parser.parse(x),
        'EPOK': lambda x: datetime.datetime.fromtimestamp(int(x)/1000),
        'TIME': lambda x: parser.parse(x),
        'STRG': lambda x: x,
        'EBOL': lambda x: x == 'True',
        'ENBL': lambda x: x == '1',
    }[typ](val)


def Convert_back(val, typ):
    """The reverse of convert. Takes a python variable and converts it to a
    string ready for the JSS.
    """
    if val:
        return {
            'BOOL': lambda x: str(x).lower(),
            'INTN': lambda x: str(x),
            'DATE': lambda x: str(x),
            'DUTC': lambda x: x.strftime("%Y-%m-%H:%M:S.%fT%X%z"),
            'EPOK': lambda x: str(int((time.mktime(x.timetuple()) * 1000))),
            'TIME': lambda x: str(x),
            'STRG': lambda x: x,
            'EBOL': lambda x: str(x),
            'ENBL': lambda x: '1' if x else '0'
        }[typ](val)
    else:
        return val


def Now():
    '''right now in datetime format.

    The sole purpose of this function is to remove the need to import
    'datetime' in your code and remember
    that it is `datetime.datetime.now()`
    just so we can get right now for comparison purposes. Yes, OK, I'm lazy.
    '''
    return datetime.datetime.now()


def Jopen(pref=None, pword=None):
    """
    Open a connection to the JSS. Asks for your password,
    returns connector. If you want to enter the URL and user
    pass it pref='True'. If you are running non-interactive pass
    it pword='password'
    """
    jss_prefs = jss.JSSPrefs()
    if pref:
        jss_prefs.url = raw_input("URL: ")
        jss_prefs.user = raw_input("User: ")
    if pword:
        jss_prefs.password = pword
    else:
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
    ['general/remote_management/management_username', 'man_username'],
    ['general/remote_management/management_password_sha256', 'man_pass'],
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
    # ['purchasing/warranty_expires', 'warranty_expires'],
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
    ['mdm', 'BOOL'],
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
    # 'Safari',  # Not Safari, sometimes updated outside a System Update
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


_c_attr_types = {
    'String': 'STRG',
    'Date': 'DATE',
    'Number': 'INTN',
}


def c_attributes(computer):
    """Returns a dictionary of the computer's extension attributes. Key is
    the attribute name.The dictionary value is a dictionary with keys 'value'
    and 'type'.
    """
    # this is starting to look a little ugly but a nicer way of hacking
    # the boolean etension attributes doesn't spring to mind.
    dict = {}
    for attr in computer.findall('extension_attributes/extension_attribute'):
        nm = attr.findtext('name')
        ty = attr.findtext('type')
        val = attr.findtext('value')
        typ = _c_attr_types[ty]
        if typ == 'STRG' and val in ['True', 'False']:
            typ = 'EBOL'
        if typ == 'STRG' and val in ['0', '1']:
            typ = 'ENBL'
        dict.update({nm: {'value': Convert(val, typ), 'type': typ}})
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


def c_remote(computer, nm, pword):
    """ sets or unsets remote management. If you pass it just the computer
    record it will set remote management to false and clear the password and
    user. Pass it a name and password and it will set remote management on with
    that user and password.
    """
    if nm:
        remote = computer.find('general/remote_management')
        add = ElementTree.SubElement(remote, "management_password")
        add.text = pword
        computer.find('general/remote_management/managed').text = 'true'
        computer.find('general/remote_management/management_username').text = nm
        computer.save()
    else:
        computer.find('general/remote_management/managed').text = 'false'
        computer.find('general/remote_management/management_username').text = ""
        computer.find('general/remote_management/management_password_sha256').text = ""


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
    ['fill_user_template', 'fut'],
    ['fill_existing_users', 'feu'],
    ['boot_volume_required', 'boot_req'],
    ['allow_uninstalled', 'uninstall'],
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


#
# iOS
#

_mobiledevices_keys = [
    'id',
    'name',
    'device_name',
    'udid',
    'serial-number',
    'phone_number',
    'wifi_mac_address',
    'managed',
    'supervised',
    'model',
    'model_identifier',
    'model_display',
    'username',
]


def m_devices(devices):
    ar = []
    for device in devices.findall('mobile_devices/mobile_device'):
        dict = {}
        for key in _mobiledevices_keys:
            dict.update({key: device.findtext(key)})
        dict['supervised'] = Convert(dict['supervised'], 'BOOL')
        dict['managed'] = Convert(dict['managed'], 'BOOL')
        ar.append(dict)
    return ar


_m_info_keys = [
    ['general/id', 'id'],
    ['general/display_name', 'display_name'],
    ['general/device_name', 'device_name'],
    ['general/name', 'name'],
    ['general/asset_tag', 'asset_tag'],
    ['general/last_inventory_update', 'last_inventory'],
    ['general/last_inventory_update_epoch', 'last_inventory_epoch'],
    ['general/capacity', 'capacity'],
    ['general/available', 'available'],
    ['general/percentage_used', 'percentage_used'],
    ['general/os_type', 'os_type'],
    ['general/os_version', 'os_version'],
    ['general/os_build', 'os_build'],
    ['general/serial_number', 'serial_number'],
    ['general/udid', 'udid'],
    ['general/initial_entry_date_epoch', 'initial_entry_epoch'],
    ['general/initial_entry_date_utc', 'initial_entry_utc'],
    ['general/phone_number', 'phone_number'],
    ['general/ip_address', 'ip_address'],
    ['general/wifi_mac_address', 'wifi_mac_address'],
    ['general/bluetooth_mac_address', 'bluetooth_mac_address'],
    ['general/modem_firmware', 'modem_firmware'],
    ['general/model', 'model'],
    ['general/model_identifier', 'model_identifier'],
    ['general/model_number', 'model_number'],
    ['general/model_display', 'model_display'],
    ['general/device_ownership_level', 'device_ownership_level'],
    ['general/last_enrollment_epoch', 'last_enrollment_epoch'],
    ['general/managed', 'managed'],
    ['general/supervised', 'supervised'],
    ['general/exchange_activesync_device_identifier', 'activesync_id'],
    ['general/shared', 'shared'],
    ['general/tethered', 'tethered'],
    ['general/ble_capable', 'ble_capable'],
    ['general/device_locator_service_enabled', 'locator_enabled'],
    ['general/do_not_disturb_enabled', 'do_not_disturb_enabled'],
    ['general/cloud_backup_enabled', 'cloud_backup_enabled'],
    ['general/last_cloud_backup_date_epoch', 'last_cloud_backupe_epoch'],
    ['general/last_cloud_backup_date_utc', 'last_cloud_backup_utc'],
    ['general/location_services_enabled', 'location_services_enabled'],
    ['general/itunes_store_account_is_active', 'itunes_account_is_active'],
    ['general/last_backup_time_epoch', 'last_backup_time_epoch'],
    ['general/site/id', 'site_id'],
    ['general/site/name', 'site_name'],
    ['location/username', 'username'],
    ['location/realname', 'realname'],
    ['location/real_name', 'real_name'],
    ['location/email_address', 'email_address'],
    ['location/position', 'position'],
    ['location/phone', 'phone'],
    ['location/phone_number', 'phone_number'],
    ['location/department', 'department'],
    ['location/building', 'building'],
    ['location/room', 'room'],
]

_m_info_convert_keys = [
    ['last_inventory', 'DATE'],
    ['last_inventory_epoch', 'EPOK'],
    ['capacity', 'INTN'],
    ['available', 'INTN'],
    ['percentage_used', 'INTN'],
    ['last_enrollment_epoch', 'EPOK'],
    ['managed', 'BOOL'],
    ['supervised', 'BOOL'],
    ['shared', 'BOOL'],
    ['tethered', 'BOOL'],
    ['ble_capable', 'BOOL'],
    ['locator_enabled', 'BOOL'],
    ['do_not_disturb_enabled', 'BOOL'],
    ['cloud_backup_enabled', 'BOOL'],
    ['last_cloud_backupe_epoch', 'EPOK'],
    ['location_services_enabled', 'BOOL'],
    ['itunes_account_is_active', 'BOOL'],
    ['last_backup_time_epoch', 'EPOK'],
]


def m_info(device):
    """Returns a a dictionary of general information about an iOS device.
    """
    dict = {}
    for key in _m_info_keys:
        dict.update({key[1]: device.findtext(key[0])})
    for dd in _m_info_convert_keys:
        dict[dd[0]] = Convert(dict[dd[0]], dd[1])
    return dict


def m_info_write(info, device):
    """Writes out any changed device info. Pass it the info
    dictionary with changed info and the object returned from
    jss.mobiledevice()
    """
    our_info = copy.deepcopy(info)
    for key in _m_info_convert_keys:
        our_info[key[0]] = Convert_back(info[key[0]], key[1])
    for key in _m_info_keys:
        device.find(key[0]).text = our_info[key[1]]
    device.save()


_m_attr_types = {
    'String': 'STRG',
    'Date': 'DATE',
    'Number': 'INTN',
}


def m_attributes(device):
    """Returns a dictionary of the device's extension attributes. Key is
    the attribute name.The dictionary value is a dictionary with keys 'value'
    and 'type'.
    """
    dict = {}
    for attr in device.findall('extension_attributes/extension_attribute'):
        nm = attr.findtext('name')
        ty = attr.findtext('type')
        val = attr.findtext('value')
        typ = _m_attr_types[ty]
        if typ == 'STRG' and val in ['True', 'False']:
            typ = 'EBOL'
        if typ == 'STRG' and val in ['0', '1']:
            typ = 'ENBL'
        dict.update({nm: {'value': Convert(val, typ), 'type': typ}})
    return dict


def m_attributes_write(attribs, device):
    """Writes out any changed extension attributes. Pass it the attribute
    dictionary with changed attributes and object returned from
    jss.mobiledevice()
    """
    for attr in device.findall('extension_attributes/extension_attribute'):
        nm = attr.findtext('name')
        val = attr.findtext('value')
        if attribs[nm]['value'] != val:
            new_val = Convert_back(attribs[nm]['value'], attribs[nm]['type'])
            attr.find('value').text = new_val
    device.save()


_m_security_keys = [
    ['security/data_protection', 'data_protection'],
    ['security/block_level_encryption_capable', 'block_encrypt_capable'],
    ['security/file_level_encryption_capable', 'file_encrypt_capable'],
    ['security/passcode_present', 'passcode_present'],
    ['security/passcode_compliant', 'passcode_compliant'],
    ['security/passcode_compliant_with_profile', 'passcode_compliant_with_profile'],
    ['security/passcode_lock_grace_period_enforced', 'passcode_lock_grace_period_enforced'],
    ['security/hardware_encryption', 'hardware_encryption'],
    ['security/activation_lock_enabled', 'activation_lock_enabled'],
    ['security/jailbreak_detected', 'jailbreak_detected'],
    ['security/lost_mode_enabled', 'lost_mode_enabled'],
    ['security/lost_mode_enforced', 'lost_mode_enforced'],
    ['security/lost_mode_enable_issued_epoch', 'lost_issued_epoch'],
    ['security/lost_mode_message', 'lost_mode_message'],
    ['security/lost_mode_phone', 'lost_mode_phone'],
    ['security/lost_mode_footnote', 'lost_mode_footnote'],
    ['security/lost_location_epoch', 'lost_location_epoch'],
    ['security/lost_location_latitude', 'lost_location_latitude'],
    ['security/lost_location_longitude', 'lost_location_longitude'],
    ['security/lost_location_altitude', 'lost_location_altitude'],
    ['security/lost_location_speed', 'lost_location_speed'],
    ['security/lost_location_course', 'lost_location_course'],
    ['security/lost_location_horizontal_accuracy', 'lost_location_horizontal_accuracy'],
    ['security/lost_location_vertical_accuracy', 'lost_location_vertical_accuracy'],
]

_m_security_convert_keys = [
    ['data_protection',  'BOOL'],
    ['block_encrypt_capable',  'BOOL'],
    ['file_encrypt_capable',  'BOOL'],
    ['passcode_present',  'BOOL'],
    ['passcode_compliant',  'BOOL'],
    ['passcode_compliant_with_profile',  'BOOL'],
    ['passcode_lock_grace_period_enforced',  'BOOL'],
    ['hardware_encryption',  'INTN'],
    ['activation_lock_enabled',  'BOOL'],
    ['jailbreak_detected',  'BOOL'],
    ['lost_mode_enforced',  'BOOL'],
    ['lost_issued_epoch',  'EPOK'],
    ['lost_location_epoch',  'EPOK'],
    ['lost_location_latitude',  'INTN'],
    ['lost_location_longitude',  'INTN'],
    ['lost_location_altitude',  'INTN'],
    ['lost_location_speed',  'INTN'],
    ['lost_location_course',  'INTN'],
    ['lost_location_horizontal_accuracy',  'INTN'],
    ['lost_location_vertical_accuracy',  'INTN'],
]


def m_security(device):
    """Returns a a dictionary of security information about an iOS device.
    """
    dict = {}
    for key in _m_security_keys:
        dict.update({key[1]: device.findtext(key[0])})
    for dd in _m_security_convert_keys:
        dict[dd[0]] = Convert(dict[dd[0]], dd[1])
    return dict


_m_network_keys = [
    ['network/home_carrier_network', 'home_carrier_network'],
    ['network/cellular_technology', 'cellular_technology'],
    ['network/voice_roaming_enabled', 'voice_roaming_enabled'],
    ['network/imei', 'imei'],
    ['network/iccid', 'iccid'],
    ['network/meid', 'meid'],
    ['network/current_carrier_network', 'current_carrier_network'],
    ['network/carrier_settings_version', 'carrier_settings_version'],
    ['network/current_mobile_country_code', 'current_mobile_country_code'],
    ['network/current_mobile_network_code', 'current_mobile_network_code'],
    ['network/home_mobile_country_code', 'home_mobile_country_code'],
    ['network/home_mobile_network_code', 'home_mobile_network_code'],
    ['network/data_roaming_enabled', 'data_roaming_enabled'],
    ['network/roaming', 'roaming'],
    ['network/phone_number', 'phone_number'],
]

_m_network_convert_keys = [
    ['voice_roaming_enabled', 'BOOL'],
    ['data_roaming_enabled', 'BOOL'],
    ['roaming', 'BOOL'],
]


def m_network(device):
    """Returns a a dictionary of network information about an iOS device.
    """
    dict = {}
    for key in _m_network_keys:
        dict.update({key[1]: device.findtext(key[0])})
    for dd in _m_network_convert_keys:
        dict[dd[0]] = Convert(dict[dd[0]], dd[1])
    return dict

