# This Python file uses the following encoding: utf-8
import unittest
from unittest import mock
import json
import service



class ServiceTestSetMessage(unittest.TestCase):
	"""Test suite for service.set_message"""

	def setUp(self):
		self.tester = service.app.test_client(self)

	def tearDown(self):
		del self.tester

	def test_set_message_badRequest(self):
		"""The client sends no-data or wrong http header"""
		response = self.tester.post('/messages', content_type='application/json')
		self.assertEqual (response.status_code, 400)
		data = '{"message": u"ɸ£utf-8"}'
		response = self.tester.post('/messages', content_type='application/json; charset=utf-16', data=data)
		self.assertEqual(response.status_code, 400)

	def test_set_message_servError(self):
		"""The DB is not available or the data is invalid"""
		with mock.patch('service.save_message', side_effect=Exception()):
			data = json.dumps({"message": u"ɸ£utf-8"})
			response = self.tester.post('/messages', content_type='application/json; charset=UTF-8', data=data)
			self.assertEqual(response.status_code, 500)

	def test_set_message_success(self):
		"""The server replies correctly"""
		mess = u"ɸ£utf-8"
		sha = service.hs.sha256(mess.encode('utf-8')).hexdigest()
		ret = {"digest": sha}
		with mock.patch('service.save_message'):
			data = json.dumps({"message": u"ɸ£utf-8"})
			response = self.tester.post('/messages', content_type='application/json; charset=UTF-8', data=data)
			self.assertEqual(response.json, ret)


class ServiceTestGetMessage(unittest.TestCase):
	"""Test suite for service.get_message"""

	def setUp(self):
		self.tester = service.app.test_client(self)

	def tearDown(self):
		del self.tester

	def test_get_message_notFound(self):
		"""The client sends no-ascii string or the digest is not found"""
		sha = '£utf-8£'
		response = self.tester.get('/messages/'+sha)
		self.assertEqual(response.status_code, 404)
		with mock.patch('service.find_message', return_value=None):
			sha = 'valid_digest'
			response = self.tester.get('/messages/'+sha)
			self.assertEqual(response.status_code, 404)

	def test_get_message_servError(self):
		"""The DB is not available"""
		with mock.patch('service.find_message', side_effect=Exception()):
			sha = 'valid_digest'
			response = self.tester.get('/messages/'+sha)
			self.assertEqual(response.status_code, 500)

	def test_get_message_success(self):
		"""The server replies correctly"""
		with mock.patch('service.find_message', return_value=b'value'):
			sha = 'digest_of_value'
			response = self.tester.get('/messages/'+sha)
			self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
	unittest.main(verbosity=2)