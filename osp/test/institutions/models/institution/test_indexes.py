

import peewee
import pytest

from osp.institutions.models import Institution


pytestmark = pytest.mark.usefixtures('db')


def test_unique_url(add_institution):

    """
    URLs should be unique.
    """

    add_institution(url='http://test.edu')

    with pytest.raises(peewee.IntegrityError):
        add_institution(url='http://test.edu')


def test_unique_domain(add_institution):

    """
    Domains should be unique.
    """

    add_institution(domain='test.edu')

    with pytest.raises(peewee.IntegrityError):
        add_institution(domain='test.edu')
