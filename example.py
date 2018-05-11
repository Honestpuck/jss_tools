# example code

import jss_tools as t
import sys

def printf(format, *args):
    sys.stdout.write(format % args)

def o_non_compliance(rec, reason):
    ''' might do something in here like email the malcontent but instead
    we'll just print something.'''
    name = rec.findtext('location/real_name')
    printf("%s\t%s", name, reason)


j = t.Jopen()

computer_list = j.Computer()

# old way
for computer in computer_list:
    this_computer = computer.retrieve()
    for attribute in this_computer.findall(
            'extension_attributes/extension_attribute'):
        # attributes for security compliance
        if attribute.findtext('name') == 'SIP status':
            if attribute.findtext('value') == 'disabled':
                o_non_cliance(this_computer, 'SIP status')
                break
        if attribute.findtext('name') == 'Carbon Black running':
            if attribute.findtext('value') in ['disabled', 'missing']:
                o_non_compliance(this_computer, 'Carbon Black')
            break
        if attribute.findtext('name') == 'Internet Sharing':
            if attribute.findtext('value') == 'Enabled':
                o_non_compliance(this_computer, 'Internet Sharing')
            break

def non_compliance(rec, reason):
    ''' might do something in here like email the malcontent but instead
    we'll just print something.'''
    computer = t.info(rec)
    name = computer['realname']
    printf("%s\t%s", name, reason)


# new way
for record in computer_list:
    computer = record.retrieve()
    attribute = t.attributes(computer)
    if attribute['SIP Status'] == 'disabled':
        non_compliance(computer, 'SIP status')
        break
    if attribute['Carbon Black Running'] in ['disabled', 'missing']:
        non_compliance(computer, 'Carbon Black')
        break
    if attribute['Internet Sharing'] == 'Enabled':
        non_compliance(computer, 'Internet Sharing')
        break


