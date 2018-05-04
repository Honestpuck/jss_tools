# example code

import jss_tools as t

j = t.Jopen()

computer_list = j.Computer()

## old way
for computer in computer_list:
    this_computer = computer.retrieve()
    for attribute in this_computer.findall('extension_attributes/extension_attribute'):
        # attributes for security compliance
        if attribute.findtext('name') == 'SIP status':
            if attribute.findtext('value') == 'disabled':
            	non_compliance(this_computer, 'SIP status')
            	break
        if attribute.findtext('name') == 'Carbon Black running':
            if attribute.findtext('value') in ['disabled', 'missing']:
            	non_compliance(this_computer, 'Carbon Black')
            break
        if attribute.findtext('name') == 'Internet Sharing':
            if attribute.findtext('value') == 'Enabled':
            	non_compliance(this_computer, 'Internet Sharing')
            break

## new way
for computer in computer_list:
    this = computer.retrieve()
    this_attr = t.attributes(this)
    if this_attr{'SIP Status'} == 'disabled':
        non_compliance(this, 'SIP status')
        break
    if this_attr{'Carbon Black Running'} in ['disabled', 'missing']:
        non_compliance(this, 'Carbon Black')
        break
    if this_attr{'Internet Sharing'} == 'Enabled':
        non_compliance(this, 'Internet Sharing')
        break

def non_compliance(rec, reason):
    ''' might do something in here like email the malcontent but instead
    we'll just print something.'''
    computer = t.info(rec)
    name = computer{'realname'}
    printf("%s\t%s", name, reason)



