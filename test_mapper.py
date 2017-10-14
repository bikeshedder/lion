from uuid import UUID

import lion

class Logo:

    def __init__(self, url, width, height):
        self.url = url
        self.width = width
        self.height = height

class Project:

    def __init__(self, id, title, logo):
        self.id = id
        self.title = title
        self.logo = logo

class Company:

    def __init__(self, id, title, logo, projects=None):
        self.id = id
        self.title = title
        self.logo = logo
        self.projects = projects or []


logo_mapper = lion.Mapper(
    lion.StrField('url'),
    lion.IntField('width'),
    lion.IntField('height'),
)

company_mapper = lion.Mapper(
    lion.UUIDField('id'),
    lion.StrField('title'),
    logo_mapper.as_field('logo', skip_cond=lambda obj: not obj.logo),
)

project_mapper = lion.Mapper(
    lion.UUIDField('id'),
    lion.StrField('title'),
    logo_mapper.as_field('logo', skip_cond=lambda obj: not obj.logo),
)

company_with_projects_mapper = lion.Mapper(
    company_mapper,
    lion.ListField('projects', mapper=project_mapper)
)


company = Company(
        id=UUID('cffa6bba-d6f9-45cb-ae20-12f31fdf2585'),
        title='Terreon GmbH',
        logo=Logo('http://terreon.de/favicon.ico', 16, 16),
        projects=[
            Project(
                id=UUID('e864b437-c861-40b6-b439-963ce6808b3e'),
                title='mushroom',
                logo=Logo(
                    url='http://mushroom.readthedocs.io/en/latest/_static/logo.png',
                    width=190,
                    height=224
                )
            ),
            Project(
                id=UUID('92b94130-f0e7-4c43-941e-845923f396e8'),
                title='lion',
                logo=None
            )
        ]
    )


def test_logo():
    assert logo_mapper(company.logo) == {
        'url': 'http://terreon.de/favicon.ico',
        'width': 16,
        'height': 16
    }

def test_company():
    assert company_mapper(company) == {
        'id': 'cffa6bba-d6f9-45cb-ae20-12f31fdf2585',
        'title': 'Terreon GmbH',
        'logo': {
            'url': 'http://terreon.de/favicon.ico',
            'width': 16,
            'height': 16
        }
    }

def test_company_with_projects():
    assert company_with_projects_mapper(company) == {
        'id': 'cffa6bba-d6f9-45cb-ae20-12f31fdf2585',
        'title': 'Terreon GmbH',
        'logo': {
            'url': 'http://terreon.de/favicon.ico',
            'width': 16,
            'height': 16
        },
        'projects': [
            {
                'id': 'e864b437-c861-40b6-b439-963ce6808b3e',
                'title': 'mushroom',
                'logo': {
                    'url': 'http://mushroom.readthedocs.io/en/latest/_static/logo.png',
                    'width': 190,
                    'height': 224
                }
            },
            {
                'id': '92b94130-f0e7-4c43-941e-845923f396e8',
                'title': 'lion',
            }
        ]
    }

def test_fields():
    fields = lion.FieldList.parse('{id,title}')
    assert company_with_projects_mapper(company, fields=fields) == {
        'id': 'cffa6bba-d6f9-45cb-ae20-12f31fdf2585',
        'title': 'Terreon GmbH',
    }

def test_fields_nested():
    fields = lion.FieldList.parse('{id,title,logo{url}}')
    assert company_with_projects_mapper(company, fields=fields) == {
        'id': 'cffa6bba-d6f9-45cb-ae20-12f31fdf2585',
        'title': 'Terreon GmbH',
        'logo': {
            'url': 'http://terreon.de/favicon.ico',
        }
    }

def test_fields_nested_list():
    fields = lion.FieldList.parse('{id,title,projects{id, title}}')
    assert company_with_projects_mapper(company, fields=fields) == {
        'id': 'cffa6bba-d6f9-45cb-ae20-12f31fdf2585',
        'title': 'Terreon GmbH',
        'projects': [
            {
                'id': 'e864b437-c861-40b6-b439-963ce6808b3e',
                'title': 'mushroom',
            },
            {
                'id': '92b94130-f0e7-4c43-941e-845923f396e8',
                'title': 'lion',
            }
        ]
    }