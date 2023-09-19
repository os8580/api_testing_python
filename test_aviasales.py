import requests
import pytest

BASE_URL = 'http://autocomplete.travelpayouts.com/places2'


@pytest.mark.parametrize('term, _type', [
    ('Mosc', 'city'),
    ('New Y', 'city'),
    ('Lond', 'city'),
    ('DME', 'airport'),
    ('CDG', 'airport'),
    ('Влад', 'city')
])
def test_autocomplete_api(term, _type):
    params = {
        'term': term,
        'locale': 'en',
        'types': _type
    }

    response = requests.get(BASE_URL, params=params)
    result = response.json()

    assert isinstance(result, list)
    assert response.status_code == 200
    for avia_type in result:
        assert 'name' in avia_type
        assert 'type' in avia_type
        assert 'code' in avia_type


def test_autocomplete_invalid_type():
    params = {
        'term': 'London',
        'locale': 'en',
        'types[]': 'invalid'
    }
    response = requests.get(BASE_URL, params=params)
    result = response.json()

    assert response.status_code == 200
    assert len(result) == 0


def test_autocomplete_no_results():
    params = {
        'term': 'Nonexistcity',
        'locale': 'en',
        'types[]': 'city'
    }
    response = requests.get(BASE_URL, params=params)
    result = response.json()

    assert response.status_code == 200
    assert isinstance(result, list)
    assert len(result) == 0


def test_autocomplete_missing_query():
    params = {
        'locale': 'en',
        'types[]': 'city'
    }
    response = requests.get(BASE_URL, params=params)

    assert response.status_code == 400
    assert response.text == 'err term contains bad characters\n'


def test_autocomplete_insensitive():
    params = {
        'term': 'moscow',
        'locale': 'en',
        'types[]': 'city'
    }
    response = requests.get(BASE_URL, params=params)
    result = response.json()

    assert response.status_code == 200
    assert isinstance(result, list)
    for avia_type in result:
        assert 'name' in avia_type
        assert 'type' in avia_type
        assert 'code' in avia_type


def test_autocomplete_incorrect_method():
    params = {
        'term': 'London',
        'locale': 'en',
        'types[]': 'city'
    }
    response = requests.post(BASE_URL, params=params)
    result = response.json()

    assert response.status_code == 200
    assert isinstance(result, list)
    for avia_type in result:
        assert 'name' in avia_type
        assert 'type' in avia_type
        assert 'code' in avia_type


def test_autocomplete_valid_locale():
    params = {
        'term': 'Лондон',
        'locale': 'ru',
        'types[]': 'city'
    }
    response = requests.post(BASE_URL, params=params)
    result = response.json()

    assert response.status_code == 200
    assert isinstance(result, list)
    for avia_type in result:
        assert 'name' in avia_type
        assert 'type' in avia_type
        assert 'code' in avia_type


def test_autocomplete_invalid_locale():
    params = {
        'term': 'Paris',
        'locale': 'srb',
        'types[]': 'city'
    }
    response = requests.post(BASE_URL, params=params)
    result = response.json()

    assert response.status_code == 200
    assert isinstance(result, list)
    for avia_type in result:
        assert 'name' in avia_type
        assert 'type' in avia_type
        assert 'code' in avia_type


def test_autocomplete_multiple_types():
    params = {
        'term': 'DME',
        'locale': 'en',
        'types[]': 'city,airport'
    }
    response = requests.post(BASE_URL, params=params)
    result = response.json()

    assert response.status_code == 200
    assert isinstance(result, list)
    for avia_type in result:
        assert isinstance(avia_type, dict)
        assert 'name' in avia_type
        assert 'type' in avia_type
        assert 'code' in avia_type
