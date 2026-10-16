import unittest
import tool

class BehaviorTests(unittest.TestCase):
    def test_case_0(self):
        self.assertEqual([x["kind"] for x in tool.analyze({'before': {}, 'after': {}})], [])

    def test_case_1(self):
        self.assertEqual([x["kind"] for x in tool.analyze({'before': {'components': [{'name': 'lib', 'version': '1'}]}, 'after': {'components': [{'name': 'lib', 'version': '2'}]}})], ['changed'])

    def test_case_2(self):
        self.assertEqual([x["kind"] for x in tool.analyze({'before': {}, 'after': {'components': [{'name': 'x'}]}})], ['added'])

    def test_missing_required_input(self):
        with self.assertRaises((KeyError, ValueError, TypeError)):
            tool.analyze({})


    def test_duplicate_identity_rejected(self):
        with self.assertRaises(ValueError): tool.analyze({'before':{},'after':{'components':[{'name':'x'},{'name':'x'}]}})
    def test_license_only_change(self):
        a={'name':'x','version':'1','licenses':[{'license':{'id':'MIT'}}]}
        b=dict(a,licenses=[{'license':{'id':'Apache-2.0'}}])
        result=tool.analyze({'before':{'components':[a]},'after':{'components':[b]}})
        self.assertEqual(result[0]['after']['licenses'],['Apache-2.0'])
