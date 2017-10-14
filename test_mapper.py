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


class LogoMapper(lion.Mapper):
    url = lion.StrField()
    width = lion.IntField()
    height = lion.IntField()

class CompanyMapper(lion.Mapper):
    id = lion.UUIDField()
    title = lion.StrField()
    logo = lion.MapperField(LogoMapper, predicate=lion.skip_none)

class ProjectMapper(lion.Mapper):
    id = lion.UUIDField()
    title = lion.StrField()
    logo = lion.MapperField(LogoMapper, predicate=lion.skip_none)

class CompanyWithProjectsMapper(CompanyMapper, lion.Mapper):
    projects = lion.ListField(ProjectMapper)


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
    assert LogoMapper().denormalize(company.logo) == {
        'url': 'http://terreon.de/favicon.ico',
        'width': 16,
        'height': 16
    }

def test_company():
    assert CompanyMapper().denormalize(company) == {
        'id': 'cffa6bba-d6f9-45cb-ae20-12f31fdf2585',
        'title': 'Terreon GmbH',
        'logo': {
            'url': 'http://terreon.de/favicon.ico',
            'width': 16,
            'height': 16
        }
    }

def test_company_with_projects():
    assert CompanyWithProjectsMapper().denormalize(company) == {
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
    fields = '{id,title}'
    assert CompanyWithProjectsMapper(fields=fields).denormalize(company) == {
        'id': 'cffa6bba-d6f9-45cb-ae20-12f31fdf2585',
        'title': 'Terreon GmbH',
    }

def test_fields_nested():
    fields = '{id,title,logo{url}}'
    assert CompanyWithProjectsMapper(fields=fields).denormalize(company) == {
        'id': 'cffa6bba-d6f9-45cb-ae20-12f31fdf2585',
        'title': 'Terreon GmbH',
        'logo': {
            'url': 'http://terreon.de/favicon.ico',
        }
    }

def test_fields_nested_list():
    fields = '{id,title,projects{id, title}}'
    assert CompanyWithProjectsMapper(fields=fields).denormalize(company) == {
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
