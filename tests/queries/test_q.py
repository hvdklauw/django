from django.db.models import F, Q
from django.test import SimpleTestCase


class QTests(SimpleTestCase):
    def test_combine_and_empty(self):
        q = Q(x=1)
        self.assertEqual(q & Q(), q)
        self.assertEqual(Q() & q, q)

    def test_combine_and_both_empty(self):
        self.assertEqual(Q() & Q(), Q())

    def test_combine_or_empty(self):
        q = Q(x=1)
        self.assertEqual(q | Q(), q)
        self.assertEqual(Q() | q, q)

    def test_combine_or_both_empty(self):
        self.assertEqual(Q() | Q(), Q())

    def test_deconstruct(self):
        q = Q(price__gt=F('discounted_price'))
        path, args, kwargs = q.deconstruct()
        self.assertEqual(path, 'django.db.models.query_utils.Q')
        self.assertEqual(args, ())
        self.assertEqual(kwargs, {'price__gt': F('discounted_price')})

    def test_deconstruct_negated(self):
        q = ~Q(price__gt=F('discounted_price'))
        path, args, kwargs = q.deconstruct()
        self.assertEqual(path, 'django.db.models.query_utils.Q')
        self.assertEqual(args, ())
        self.assertEqual(kwargs, {
            'price__gt': F('discounted_price'),
            '_negated': True,
        })

    def test_deconstruct_or(self):
        q1 = Q(price__gt=F('discounted_price'))
        q2 = Q(price=F('discounted_price'))
        q = q1 | q2
        path, args, kwargs = q.deconstruct()
        self.assertEqual(path, 'django.db.models.query_utils.Q')
        self.assertEqual(args, (
            ('price__gt', F('discounted_price')),
            ('price', F('discounted_price')),
        ))
        self.assertEqual(kwargs, {'_connector': 'OR'})

    def test_deconstruct_and(self):
        q1 = Q(price__gt=F('discounted_price'))
        q2 = Q(price=F('discounted_price'))
        q = q1 & q2
        path, args, kwargs = q.deconstruct()
        self.assertEqual(path, 'django.db.models.query_utils.Q')
        self.assertEqual(args, (
            ('price__gt', F('discounted_price')),
            ('price', F('discounted_price')),
        ))
        self.assertEqual(kwargs, {'_connector': 'AND'})

    def test_deconstruct_and_2(self):
        q = Q(price__gt=F('discounted_price'), price=F('discounted_price'))
        path, args, kwargs = q.deconstruct()
        self.assertEqual(path, 'django.db.models.query_utils.Q')
        self.assertEqual(args, (
            ('price__gt', F('discounted_price')),
            ('price', F('discounted_price')),
        ))
        self.assertEqual(kwargs, {'_connector': 'AND'})

    def test_deconstruct_nested(self):
        q = Q(Q(price__gt=F('discounted_price')))
        path, args, kwargs = q.deconstruct()
        self.assertEqual(path, 'django.db.models.query_utils.Q')
        self.assertEqual(args, (Q(price__gt=F('discounted_price')),))
        self.assertEqual(kwargs, {'_connector': 'AND'})

    def test_reconstruct(self):
        q = Q(price__gt=F('discounted_price'))
        path, args, kwargs = q.deconstruct()
        self.assertEqual(Q(*args, **kwargs), q)

    def test_reconstruct_negated(self):
        q = ~Q(price__gt=F('discounted_price'))
        path, args, kwargs = q.deconstruct()
        self.assertEqual(Q(*args, **kwargs), q)

    def test_reconstruct_or(self):
        q1 = Q(price__gt=F('discounted_price'))
        q2 = Q(price=F('discounted_price'))
        q = q1 | q2
        path, args, kwargs = q.deconstruct()
        self.assertEqual(Q(*args, **kwargs), q)

    def test_reconstruct_and(self):
        q1 = Q(price__gt=F('discounted_price'))
        q2 = Q(price=F('discounted_price'))
        q = q1 & q2
        path, args, kwargs = q.deconstruct()
        self.assertEqual(Q(*args, **kwargs), q)
