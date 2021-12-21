"""
Get the Amazon root CA certificate
"""
import os

def aws_get_root_ca_cert_filename(name="AmazonRootCA3"):
    """
    Get root CA certificate filename

    :param name: Name of certificate (Amazon has more than one). The default is the only
                 one bundled now, but more may be added if required.
    :returns: Certificate file full pathname
    """
    installdir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(installdir, "ca_certs", f"{name}.pem")


def aws_get_root_ca_cert(name="AmazonRootCA3"):
    """
    Get the AWS root CA certificate

    :param name: Name of certificate (Amazon has more than one). The default should normally be used.
    :returns: Certificate as a string in PEM format
    """
    with open(aws_get_root_ca_cert_filename(name), "r") as cert:
        return cert.read()
