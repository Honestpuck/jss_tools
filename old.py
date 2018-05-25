#
# old way
#


def non_compliance(rec, reason):
    mac_name = rec.findtext('general/name')
    name = rec.findtext('location/real_name')
    email = rec.findtext('location/email_address')
    os = rec.findtext('hardware/os_version')
    build = rec.findtext('hardware/os_build')
    printf("%s\t%s\t%s\t%s\t%s-%s\n", mac_name, name, email, reason, os, build)


def check_one(rec):
    OS13BUILD = 97416
    OS12BUILD = 94067

    os = rec.findtext('hardware/os_version')
    build = rec.findtext('hardware/os_build')
    if StrictVersion(os) < StrictVersion('10.12.6'):
        non_compliance(rec, 'os_upgrade')
        return
    if 'G' in build:
        return
    if StrictVersion(os) > StrictVersion('10.13.0') and (
            build < OS13BUILD):
        non_compliance(rec, 'os_update')
        return
    if (StrictVersion(os) > StrictVersion('10.12.0')) and (
            build < OS12BUILD):
        non_compliance(rec, 'os_update')
        return
