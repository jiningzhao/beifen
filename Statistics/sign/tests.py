from django.test import TestCase
from sign.models import Event, Guest


# Create your tests here.
class ModelTest(TestCase):
    # 当Django在执行setUp()部分的操作时，并不会真正地向数据库中插入数据。所以不用关心产生测试数据之后的清理工作
    def setUp(self):
        Event.objects.create(id=1, name='oneplus 3 event', status=True, limit=2000, address='shenzhen',
                             start_time='2016-08-31 02:18:22')
        Guest.objects.create(id=1, event_id=1, realname='alen234', phone='1371101101', email='alen@mail.com',
                             sign=False)

    def test_event_models(self):
        result = Event.objects.get(name='oneplus 3 event')
        self.assertEqual(result.address, "shenzhen")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='1371101101')
        self.assertEqual(result.realname, 'alen234')
        self.assertFalse(result.sign)
