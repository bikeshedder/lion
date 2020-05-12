from uuid import UUID

import lion


class BaseObj:
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class Logo(BaseObj):
    def __init__(self, url=None, width=None, height=None):
        self.url = url
        self.width = width
        self.height = height

class Project(BaseObj):
    def __init__(self, id=None, title=None, logo=None):
        self.id = id
        self.title = title
        self.logo = logo

class Company(BaseObj):
    def __init__(self, id=None, title=None, logo=None, projects=None):
        self.id = id
        self.title = title
        self.logo = logo
        self.projects = projects or []


class LogoMapper(lion.Mapper):
    factory = Logo
    url = lion.StrField()
    width = lion.IntField()
    height = lion.IntField()

class CompanyMapper(lion.Mapper):
    factory = Company
    id = lion.UUIDField()
    title = lion.StrField()
    logo = lion.MapperField(LogoMapper, condition=lion.skip_none)

class ProjectMapper(lion.Mapper):
    factory = Project
    id = lion.UUIDField()
    title = lion.StrField()
    logo = lion.MapperField(LogoMapper, condition=lion.skip_none)

class CompanyWithProjectsMapper(CompanyMapper, lion.Mapper):
    factory = Company
    projects = lion.ListField(ProjectMapper)


class Node(BaseObj):
    def __init__(self, id=None, title=None, parent=None, children=None):
        self.id = id
        self.title = title
        self.parent = parent
        self.children = children or []

class NodeMapper(lion.Mapper):
    factory = Node
    id = lion.UUIDField()
    title = lion.StrField()
    parent = lion.MapperField('self', condition=lion.skip_none)
    children = lion.ListField('self', condition=lion.skip_empty)


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

node = Node(
    id=UUID('778fc992-76b9-47d0-88a2-16392741b6fc'),
    title='parent',
    parent=Node(
        id=UUID('5824dc9f-0588-4b67-bcb2-b40e4de6bbf9'),
        title='root'
    ),
    children=[
        Node(
            id=UUID('01132f38-1b16-4747-a80c-38323852c570'),
            title='first_child'
        ),
        Node(
            id=UUID('96016eb7-914b-42d4-b787-1fca52fe29c2'),
            title='second_child'
        ),
    ]
)


def test_logo():
    assert LogoMapper().dump(company.logo) == {
        'url': 'http://terreon.de/favicon.ico',
        'width': 16,
        'height': 16
    }

def test_company():
    assert CompanyMapper().dump(company) == {
        'id': 'cffa6bba-d6f9-45cb-ae20-12f31fdf2585',
        'title': 'Terreon GmbH',
        'logo': {
            'url': 'http://terreon.de/favicon.ico',
            'width': 16,
            'height': 16
        }
    }

def test_company_with_projects():
    data = CompanyWithProjectsMapper().dump(company)
    assert data == {
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
    assert CompanyWithProjectsMapper().load(data) == company

def test_node():
    data = NodeMapper().dump(node)
    assert data == {
        'id': '778fc992-76b9-47d0-88a2-16392741b6fc',
        'title': 'parent',
        'parent': {
            'id': '5824dc9f-0588-4b67-bcb2-b40e4de6bbf9',
            'title': 'root'
        },
        'children': [
            {
                'id': '01132f38-1b16-4747-a80c-38323852c570',
                'title': 'first_child'
            },
            {
                'id': '96016eb7-914b-42d4-b787-1fca52fe29c2',
                'title': 'second_child'
            },
        ]
    }
    assert NodeMapper().load(data) == node

def test_fields():
    fields = '{id,title}'
    assert CompanyWithProjectsMapper(fields=fields).dump(company) == {
        'id': 'cffa6bba-d6f9-45cb-ae20-12f31fdf2585',
        'title': 'Terreon GmbH',
    }

def test_fields_nested():
    fields = '{id,title,logo{url}}'
    assert CompanyWithProjectsMapper(fields=fields).dump(company) == {
        'id': 'cffa6bba-d6f9-45cb-ae20-12f31fdf2585',
        'title': 'Terreon GmbH',
        'logo': {
            'url': 'http://terreon.de/favicon.ico',
        }
    }

def test_fields_nested_list():
    fields = '{id,title,projects{id, title}}'
    assert CompanyWithProjectsMapper(fields=fields).dump(company) == {
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

def test_fields_recursive():
    fields = '{id,parent{id},children{id}}'
    assert NodeMapper(fields=fields).dump(node) == {
        'id': '778fc992-76b9-47d0-88a2-16392741b6fc',
        'parent': {
            'id': '5824dc9f-0588-4b67-bcb2-b40e4de6bbf9',
        },
        'children': [
            {
                'id': '01132f38-1b16-4747-a80c-38323852c570',
            },
            {
                'id': '96016eb7-914b-42d4-b787-1fca52fe29c2',
            },
        ]
    }
