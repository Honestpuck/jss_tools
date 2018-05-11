# example code

import jss_tools as t

j = t.Jopen()

computer_list = j.Computer()

# old way
attr = 'extension_attributes/extension_attribute'
for computer in computer_list:
    this_computer = computer.retrieve()
    for attribute in this_computer.findall(attr):
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

# new way
for record in computer_list:
    computer = record.retrieve()
    attribute = t.attributes(computer)
    if attribute{'SIP Status'} == 'disabled':
        non_compliance(computer, 'SIP status')
        break
    if attribute{'Carbon Black Running'} in ['disabled', 'missing']:
        non_compliance(computer, 'Carbon Black')
        break
    if attribute{'Internet Sharing'} == 'Enabled':
        non_compliance(computer, 'Internet Sharing')
        break


def non_compliance(rec, reason):
    ''' might do something in here like email the malcontent but instead
    we'll just print something.'''
    computer = t.info(rec)
    name = computer{'realname'}
    printf("%s\t%s", name, reason)
