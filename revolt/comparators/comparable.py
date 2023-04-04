import inspect

from niltype import Nil


class Delayed:
    def __init__(self, l):
        self.l = l

    def __bool__(self):
        return self.l()

    def __repr__(self):
        return f'{inspect.getsource(self.l)} -> {bool(self)}'


class NonComparable:
    def __eq__(self, other):
        return False

    def __bool__(self):
        return False


class ComparableProp:
    def __init__(self, schema, name):
        self.schema = schema
        self.name = name

    def len(self):
        if self.schema.props.value:
            return len(getattr(self.schema.props, self.name))
        return NonComparable()

    def __bool__(self):
        if getattr(self.schema.props, self.name) != Nil:
            return True
        return False

    def get(self):
        if not hasattr(self.schema.props, self.name):
            return NonComparable()
        return getattr(self.schema.props, self.name)


class Comparable:
    def __init__(self, schema):
        self.schema = schema

    def prop(self, name):
        return ComparableProp(self.schema, name)

    def has(self, name):
        return hasattr(self.schema.props, name) and getattr(self.schema.props, name) != Nil
