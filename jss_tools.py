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
# required for colored
import os

def Jopen():
    ''' Open a connection to the JSS. Asks for your password, returns connector
    '''
    jss_prefs = jss.JSSPrefs()
    jss_prefs.password = getpass.getpass()
    return jss.JSS(jss_prefs)

# list of general XML keys and a short form. Short form becomes dictioary key.
__computer_keys = [
    # general
    ['general/id', 'id' ],          # JAMF ID
    ['general/name', 'name' ],
    ['general/mac_address', 'mac' ],
    ['general/alt_mac_address', 'mac2' ],
    ['general/ip_address', 'ip' ],
    ['general/serial_number', 'serial' ],
    ['general/barcode_1', 'bar1' ],
    ['general/barcode_2', 'bar2' ],
    ['general/asset_tag', 'tag' ],
    ['general/remote_management/managed', 'managed' ],
    ['general/mdm_capable', 'mdm' ],
    ['general/last_contact_time', 'last' ],
    ['general/initial_entry_date', 'initial' ],
    ['hardware/model', 'model' ],
    ['hardware/model_identifier', 'model_id' ],
    ['hardware/os_version', 'os' ],
    ['hardware/os_build', 'os_build' ],
    ['hardware/master_password_set', 'master' ],
    ['hardware/active_directory_status', 'AD' ],
    ['hardware/institutional_recovery_key', 'recovery' ],
    # user
    ['location/username', 'user'],
    ['location/real_name', 'name'],
    ['location/email_address', 'email'],
    # purchasing
#     ['purchasing/is_purchased', 'purchased'],
#     ['purchasing/is_leased', 'leased'],
#     ['purchasing/po_number', 'po_num'],
#     ['purchasing/vendor', 'vendor'],
#     ['purchasing/applecare_id', 'applecare'],
#     ['purchasing/purchase_price', 'price'],
#     ['purchasing/purchasing_account', 'pur_account'],
#     ['purchasing/po_date', 'po_date'],
#     ['purchasing/warranty_expires', 'warranty'],
#     ['purchasing/lease_expires', 'lease'],
#     ['purchasing/purchasing_contact', 'pur_contact'],
#     ['purchasing/os_applecare_id', 'applecare'],
#     ['purchasing/os_maintenance_expires', 'maintenance']
]

# general information
def info(rec, keys=__computer_keys):
    dict = {}
    for key in keys:
        value = args[0].findtext(key[0])
        dict.update( {key[1] : value})
    return dict

# apps to ignore in app list (Apple apps)
__ignore_apps = [
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
#    'Self Service',
    # MS
#     'Microsoft Excel',
#     'Microsoft OneNote',
#     'Microsoft Outlook',
#     'Microsoft PowerPoint',
#     'Microsoft Teams',
#     'Microsoft Word',
#     'OneDrive',
#     'Skype for Business',
]

def apps(rec, ignore=__ignore_apps):
    ''' apps(computer, ignore)
    Returns a dictionary of the apps installed. Key is name and value is version.
    It ignores the Apple apps or the apps listed in the optional paramater 'ignore',
    which is an array of app names to ignore.
    '''
    dict = {}
    for app in rec.findall('software/applications/application'):
        nm = app.findtext('name').split('.')[0]
        vers = app.findtext('version')
        if nm not in ignore:
            dict.update({nm : vers})
    return dict

def attributes(computer):
    ''' Returns a dictionary of the computers extension attributes. Each is added
    twice so you can get the value by the attribute name or id. Only gives you
    the value, not the type.
    '''
    dict = {}
    for attr in computer.findall('extension_attributes/extension_attribute'):
        id = attr.findtext('id')
        nm = attr.findtext('name')
        type = attr.findtext('type')
        val = attr.findtext('value')
        if type == 'Number':
            eval = int(val)
        else:
            eval = value
        dict.update({id: eval, nm: eval})
    return dict

def groups(computer):
    ''' Returns an array of the computer groups computer belongs to.
    '''
    # groups is borked somehow so handle differently
    ar = []
    ls = computer.findall('groups_accounts/computer_group_memberships')
    ll = ls[0]
    for group in ll:
        ar.append(group.text)
    return ar

__pak_keys = [
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

def package(rec, keys=__pak_keys):
    dict = {}
    for key in keys:
        value = rec.findtext(key[0])
        dict.update( {key[1] : value})
    return dict

__pol_keys = [
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
__pol_pak_keys = [
    'id',
    'name',
    'action',
    'fut',
    'feu',
    'autorun',
]
__pol_script_keys = [
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

def policy(rec, keys=__pol_keys):
    dict = {}
    for key in keys:
        value = rec.findtext(key[0])
        dict.update( {key[1] : value})
    # build list of packages in policy
    paks = []
    if dict['pak_count'] == 0
        paks = [None]
    else:
        for ar in rec.findall('package_configuration/packages/package'):
            pak = ar[0]
            for pak_key in __pol_pak_keys:
                value = pak.findtext(pak_key)
                paks.update( {pak_key : value})
    dict.update( {'paks' : paks})
    # build list of scripts in policy
    scripts = []
    if dict['script_count'] == 0
        scripts = [None]
    else:
        for ar in rec.findall('scripts/script'):
            script = ar[0]
            for s_key in __pol_script_keys:
                value = script.findtext(s_key)
                scripts.update( {s_key : value})
    dict.update( {'scripts' : scripts})
    return dict

__script_keys = [
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

def script(rec, keys=__script_keys)
    dict = {}
    for key in keys:
        value = rec.findtext(key[0])
        dict.update( {key[1] : value})
    return dict

# thanks to vfuse for this function
def colored(text, color=None):
    ''' return 'text' surrounded by ANSI color commands to set
    text to 'color'
    '''
    if not os.getenv('ANSI_COLORS_DISABLED'):
        fmt_str = '\033[%dm'
        reset = '\033[0m'
        colors = {
            'grey': 30,
            'gray': 30,
            'red': 31,
            'green': 32,
            'yellow': 33,
            'blue': 34,
            'magenta': 35,
            'cyan': 36,
            'white': 37,
        }
        if color is not None:
            text = fmt_str % (colors[color]) + text + reset
    return text



