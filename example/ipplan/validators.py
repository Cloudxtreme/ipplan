import netaddr

from django.core.exceptions import ValidationError


def validate_cidr(value):
    """
    Checks whether value is in CIDR notation

    value    input value from form.
    Return   None
    """
    try:
        network = netaddr.IPNetwork(value)
    except netaddr.core.AddrFormatError:
        raise ValidationError('%s is not a valid CIDR' % value)
    # Check if host bits are set in a network that is eq or gt /24
    netmask = network.netmask
    if network.ip.words[3] != 0 and netmask <= netaddr.IPAddress('255.255.255.0'):
        raise ValidationError('Host bits are set while netmask is larger than /25')
