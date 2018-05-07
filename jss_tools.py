#
# JSS_tools.py
#
# functions to turn a JSS records into more useful
# python variables, mostly dictionaries and arrays.
#
# Tony Williams (ARW)
#
# 3 May 2018
# v1.0

# required for jss
import jss
import getpass


def Jopen():
    ''' Open a connection to the JSS. Asks for your password, returns connector
    '''
    jss_prefs = jss.JSSPrefs()
    jss_prefs.password = getpass.getpass()
    return jss.JSS(jss_prefs)


# Routines for the computer record

# list of general XML keys and a short form. Short form becomes dictionary key.
# this sort of thing is used a lot in here.
_computer_keys = [
    # general
    ['general/id', 'id'],          # JAMF ID
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


# general information
def info(rec, keys=_computer_keys):
    dict = {}
    for key in keys:
        dict.update({key[1]: rec.findtext(key[0])})
    return dict


# apps to ignore in app list (Apple apps)
_ignore_apps = [
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


def apps(rec, ignore=_ignore_apps):
    '''Returns a dictionary of the apps installed. Key is name and value is
    version. It ignores the Apple apps or the apps listed in the optional
    paramater 'ignore', which is an array of app names to ignore.
    '''
    dict = {}
    for app in rec.findall('software/applications/application'):
        nm = app.findtext('name').split('.')[0]
        if nm not in ignore:
            dict.update({nm: app.findtext('version')})
    return dict


def attributes(rec):
    '''Returns a dictionary of the computers extension attributes. Each is
    added twice so you can get the value by the attribute name or id. Only
    gives you the value, not the type.
    '''
    dict = {}
    for attr in rec.findall('extension_attributes/extension_attribute'):
        id = attr.findtext('id')
        nm = attr.findtext('name')
        val = attr.findtext('value')
        dict.update({id: val, nm: val})
    return dict


def groups(rec):
    ''' Returns an array of the computer groups computer belongs to.
    '''
    ar = []
    for group in rec.find('groups_accounts/computer_group_memberships'):
        ar.append(group.text)
    return ar


_user_keys = [
    'name',
    'realname',
    'uid',
    'home',
    'home_size_mb',
    'administrator',
    'file_vault_enabled',
]


def users(rec):
    ar = []
    for u in rec.find('groups_accounts/local_accounts'):
        if u.findtext('name')[0] is not '_':
            dict = {}
            for key in _user_keys:
                dict.update({key: u.findtext(key)})
            ar.append(dict)
    return ar


_cert_keys = [
    ['common_name', 'name'],
    ['identity', 'identity'],
    ['expires_utc', 'utc'],
    ['expires_epoch', 'epoch'],
    ['name', 'name'],
]


def certificates(rec):
    ar = []
    for cert in rec.findall('cetificates/certificate'):
        dict = {}
        for key in _cert_keys:
            dict.update({key[1]: rec.findtext(key[0])})
            ar.append(dict)
    return ar


_prof_keys = [
    'id',
    'name',
    'uuid',
    'is_removable'
]


def profiles(rec, keys=_prof_keys):
    ar = []
    for profile in rec.findall('configuration_profiles/configuration_profile'):
        dict = {}
        for key in _prof_keys:
            dict.update({key: profile.findtext(key)})
        ar.append(dict)
    return ar


# Other record types

_pak_keys = [
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


def package(rec, keys=_pak_keys):
    dict = {}
    for key in keys:
        dict.update({key[1]: rec.findtext(key[0])})
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
    'paramater4',
    'paramater5',
    'paramater6',
    'paramater7',
    'paramater8',
    'paramater9',
    'paramater10',
    'paramater11',
]


def policy(rec, keys=_pol_keys):
    dict = {}
    for key in keys:
        value = rec.findtext(key[0])
        dict.update({key[1]: value})
    # build list of packages in policy
    paks = []
    if dict['pak_count'] == '0':
        paks = [None]
    else:
        for pak in rec.findall('package_configuration/packages/package'):
            for pak_key in _pol_pak_keys:
                value = pak.findtext(pak_key)
                paks.update({pak_key: value})
    dict.update({'paks': paks})
    # build list of scripts in policy
    scripts = []
    if dict['script_count'] == '0':
        scripts = [None]
    else:
        for script in rec.findall('scripts/script'):
            for s_key in _pol_script_keys:
                value = script.findtext(s_key)
                scripts.update({s_key: value})
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


def script(rec, keys=_script_keys):
    dict = {}
    for key in keys:
        value = rec.findtext(key[0])
        dict.update({key[1]: value})
    return dict
