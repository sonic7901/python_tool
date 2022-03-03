import whois
import socket
import urllib.parse


def read_ip(input_domain):
    if 'http' in input_domain:
        input_domain = urllib.parse.urlparse(input_domain).netloc
    return socket.gethostbyname(input_domain)


def read_org(input_domain):
    if 'http' in input_domain:
        input_domain = urllib.parse.urlparse(input_domain).netloc
    temp_dict = whois.whois(input_domain)
    print(temp_dict)
    if 'org' in temp_dict:
        return temp_dict['org']
    else:
        return ''


def read_country(input_domain):
    if 'http' in input_domain:
        input_domain = urllib.parse.urlparse(input_domain).netloc
    temp_dict = whois.whois(input_domain)
    if 'country' in temp_dict:
        return temp_dict['country']
    else:
        return ''


if __name__ == '__main__':
    print(read_org('http://tour.yunlin.gov.tw'))
    print(read_country('http://tour.yunlin.gov.tw'))
    print(read_ip('http://tour.yunlin.gov.tw'))
