#!/usr/bin/env python

import unittest
import os.path
import jobs


class Yr(unittest.TestCase):

    def setUp(self):
        xml_path = os.path.join(os.path.dirname(__file__), 'test_data',
                                'varsel.xml')
        with open(xml_path, 'r') as f:
            self.xml = f.read()

    def test_parse(self):
        yr = jobs.Yr({'interval': None, 'url': None})
        data = yr._parse(self.xml)

        self.assertEqual('Delvis skyet', data['description'])
        self.assertEqual('Trondheim', data['location'])
        self.assertEqual('16.3', data['temperature'])
        self.assertEqual('Nord', data['wind']['direction'])
        self.assertEqual('0.7', data['wind']['speed'])
        self.assertEqual('Flau vind', data['wind']['description'])


if __name__ == '__main__':
    unittest.main()
