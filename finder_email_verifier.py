"""Client for searching and verifying emails."""

import requests

API_KEY = 'e3072867b4808be5e694697d2ffa683e026d9ecb'
URL_VERIFY = 'https://api.hunter.io/v2/email-verifier'
URL_DOMAIN_SEARCH = 'https://api.hunter.io/v2/domain-search'

verify_emails = {}
emails_by_domain = {}


def verify_email(email: str) -> str:
    """Do email verification and validation.

    :param email: validation email
    :return: str
    """
    params_api = {'api_key': API_KEY, 'email': email}
    try:
        response = requests.get(url=URL_VERIFY, params=params_api, timeout=10)
    except requests.RequestException:
        raise requests.RequestException()
    response.raise_for_status()
    data_response = response.json()
    return data_response['data']['status']


def create_verify_email(email: str) -> None:
    """Add a new e-mail entry to the dictionary.

    :param email: validation email
    :return: None
    """
    if email not in verify_emails:
        status_email = verify_email(email)
        verify_emails[email] = status_email
    else:
        raise KeyError(email, 'already exists in the database')


def read_verify_email(email: str = None) -> dict | str:
    """Let's read the dictionary with the entries.

    :return: dict or str
    """
    if email is None:
        return verify_emails
    return verify_emails.get(email)


def update_verify_email(email: str) -> None:
    """Let's update the e-mail data in the dictionary.

    :param email: validation email
    :return: None
    """
    if email not in verify_emails:
        raise KeyError('No result found for', email)
    else:
        check_email = verify_email(email)
        verify_emails[email] = check_email


def delete_verify_email(email: str) -> None:
    """Let's remove the e-mail data from the dictionary.

    :param email: validation email
    :return: None
    """
    if email in verify_emails:
        verify_emails.pop(email)
    else:
        raise KeyError('No result found for', email)


def search_emails_by_domain(domain: str) -> str:
    """Find emails by domain name.

    :param domain: email address lookup domain
    :return: str
    """
    params_search = {'domain': domain, 'api_key': API_KEY}
    try:
        response = requests.get(URL_DOMAIN_SEARCH, params=params_search, timeout=10)
    except requests.RequestException:
        raise requests.RequestException()
    response.raise_for_status()
    data_response = response.json()
    return data_response['data']['emails']


def create_emails_by_domain(domain: str) -> None:
    """Let's add the domain with the list of emails to the database.

    :param domain: email address lookup domain
    :return: None
    """
    if domain not in emails_by_domain:
        emails = search_emails_by_domain(domain)
        emails_by_domain[domain] = [email['value'] for email in emails]
    else:
        raise KeyError(domain, 'already exists in the database')


def read_emails_by_domain(domain: str = None) -> dict:
    """Let's read the data from the database.

    :return: data dictionary
    """
    if domain is None:
        return emails_by_domain
    return emails_by_domain.get(domain)


def update_emails_by_domain(domain: str) -> None:
    """Update the email address of the domain in our database.

    :param domain: domain name in the database
    :return: None
    """
    if domain in emails_by_domain:
        emails = search_emails_by_domain(domain)
        emails_by_domain[domain] = [email['value'] for email in emails]
    else:
        raise KeyError('No result found for', domain)


def delete_emails_by_domain(domain: str) -> None | str:
    """Delete domain email addresses in our database.

    :param domain: domain name in the database
    :return: None or str
    """
    if domain in emails_by_domain:
        emails_by_domain.pop(domain)
    else:
        return 'The domain does not exist in the database.'


if __name__ == '__main__':
    create_verify_email('patrick@stripe.com')
    print(read_verify_email())
    update_verify_email('patrick@stripe.com')
    print(read_verify_email())
    delete_verify_email('patrick@stripe.com')
    print(read_verify_email())

    create_emails_by_domain('google.com')
    create_emails_by_domain('hunter.io')
    print(read_emails_by_domain())
    delete_emails_by_domain('google.com')
    print(read_emails_by_domain())
    update_emails_by_domain('github.com')
