"""Module that checks email addresses."""
import requests


class EmailVerifier(object):
    """The class performs email verification and validation."""

    def __init__(self, api_key: str) -> None:
        """Initialize the EmailVerifier class.

        :param api_key: api key of the hunter io.
        """
        self.api_key = api_key
        self.url_verify = 'https://api.hunter.io/v2/email-verifier'
        self.database_verify = {}

    def check_valid_email(self, email: str) -> bool | str:
        """Do email verification and validation.

        :param email: validation email
        :return: bool
        """
        params_api = {'api_key': self.api_key, 'email': email}
        try:
            data_api = requests.get(url=self.url_verify, params=params_api, timeout=10).json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return 'Ops...something went wrong...'
        return data_api['data']['status'] == 'valid'

    def create(self, email: str) -> None | str:
        """Add a new e-mail entry to the dictionary.

        :param email: validation email
        :return: None or str
        """
        if email not in self.database_verify:
            check_email = self.check_valid_email(email)
            self.database_verify[email] = 'valid' if check_email else 'invalid'
        else:
            return 'Email there is in database'

    def read(self) -> dict:
        """Let's read the dictionary with the entries.

        :return: dict
        """
        return self.database_verify

    def update(self, email: str) -> None | str:
        """Let's update the e-mail data in the dictionary.

        :param email: validation email
        :return: None or str
        """
        if email not in self.database_verify:
            return 'Ops...email does not exist in database.'
        else:
            check_email = self.check_valid_email(email)
            self.database_verify[email] = 'valid' if check_email else 'invalid'

    def delete(self, email: str) -> None | str:
        """Let's remove the e-mail data from the dictionary.

        :param email: validation email
        :return: None or str
        """
        if email in self.database_verify:
            self.database_verify.pop(email)
        else:
            return 'Email does not exist in database.'


class DomainSearch(object):
    """The class searches for email addresses by a given domain."""

    def __init__(self, api_key):
        """Initialize the DomainSearch class.

        :param api_key: api key of the hunter io.
        """
        self.api_key = api_key
        self.url = 'https://api.hunter.io/v2/domain-search'
        self.database = {}

    def search_emails(self, domain: str) -> str | dict:
        """Find emails by domain name.

        :param domain: email address lookup domain
        :return: None or dict of result
        """
        params_search = {'domain': domain, 'api_key': self.api_key}
        try:
            data_search = requests.get(self.url, params=params_search, timeout=10).json()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            return 'Ops...something went wrong...'
        return data_search['data']['emails']

    def create(self, domain: str) -> None | str:
        """Let's add the domain with the list of emails to the database.

        :param domain: email address lookup domain
        :return: None or str
        """
        if domain not in self.database:
            emails = self.search_emails(domain)
            self.database[domain] = [email['value'] for email in emails]
        else:
            return 'Domain already exists in the database.'

    def read(self) -> dict:
        """Let's read the data from the database.

        :return: data dictionary
        """
        return self.database

    def update(self, domain: str) -> None | str:
        """Update the email address of the domain in our database.

        :param domain: domain name in the database
        :return: None or str
        """
        if domain in self.database:
            emails = self.search_emails(domain)
            self.database[domain] = [email['value'] for email in emails]
        else:
            return 'The domain does not exist in the database. You need to create it first.'

    def delete(self, domain: str) -> None | str:
        """Delete domain email addresses in our database.

        :param domain: domain name in the database
        :return: None or str
        """
        if domain in self.database:
            self.database.pop(domain)
        else:
            return 'The domain does not exist in the database.'


apikey = 'e3072867b4808be5e694697d2ffa683e026d9ecb'
