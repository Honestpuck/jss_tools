
_computer_management_keys = [
    ['general/id', 'id'],
    ['general/name', 'name'],
    ['general/udid', 'udid'],
    ['general/serial_number', 'serial'],
    ['general/mac_address', 'mac'],
]

_computer_management_pol_keys = [
    'id',
    'name',
    'triggers',
    ]

_computer_management_profile_keys = [
    'id',
    'name',
]

_computer_management_group_keys = [
    'id',
    'name',
]


def computer_management(computer):
    """Returns a dictionary from a computer management record. The key
    'policies' has an array of info re: the policies on the machine, the key
    'config' on configuration profiles, 'smart' has the smart groups and
    'static' the static groups for the Mac.
    """
    dict = {}
    for key in _computer_management_keys:
        dict.update({key[1]: computer.findtext(key[0])})
    pol_ar = []
    for pol in computer.findall('policies/policy'):
        pol_dict = {}
        for pol_key in _computer_management_pol_keys:
            pol_dict.update({pol_key[1]: computer.findtext(pol_key[0])})
        pol_ar.append(pol_dict)
    dict.update({'policies': pol_ar})
    prof_ar = []
    for prof in computer.findall('os_x_configuration_profiles/profile'):
        prof_dict = {}
        for prof_key in _computer_management_profile_keys:
            pol_dict.update({prof_key[1]: computer.findtext(prof_key[0])})
        prof_ar.append(prof_dict)
    dict.update({'config': prof_ar})
    sm_ar = []
    for smart in computer.findall('smart_groups/group'):
        sm_dict = {}
        for sm_key in _computer_management_group_keys:
            sm_dict.update({sm_key[1]: computer.findtext(sm_key[0])})
        sm_ar.append(sm_dict)
    dict.update({'smart': sm_ar})
    st_ar = []
    for static in computer.findall('static_groups/group'):
        st_dict = {}
        for st_key in _computer_management_group_keys:
            st_dict.update({sm_key[1]: computer.findtext(st_key[0])})
        st_ar.append(st_dict)
    dict.update({'static': st_ar})
