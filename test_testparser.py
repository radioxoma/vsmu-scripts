#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import io
import unittest
import testparser


class TestEvsmu(unittest.TestCase):
    def setUp(self):
        """Sorting inconsistent if there are equal questions text but
        different answers.
        """
        self.quiz_evsmu = testparser.parse_evsmu("tests/evsmu/g495.htm")
        self.quiz_evsmu.sort(key=lambda q: q.question.lower())

    def test_evsmu_to_mytestx_output(self):
        with io.open('tests/evsmu/g495_mytestx.txt', encoding='cp1251') as f:
            self.assertEqual(f.read(), testparser.to_mytestx(self.quiz_evsmu))

    def test_evsmu_to_anki_output(self):
        with io.open('tests/evsmu/g495_anki.csv') as f:
            self.assertEqual(f.read(), testparser.to_anki(self.quiz_evsmu))

    def test_evsmu_to_crib_output(self):
        with io.open('tests/evsmu/g495_crib.txt') as f:
            self.assertEqual(f.read(), testparser.to_crib(self.quiz_evsmu))


class TestDo(unittest.TestCase):
    def setUp(self):
        self.quiz_do = testparser.parse_do("tests/do/g100_do_pic.htm")
        self.quiz_do.sort(key=lambda q: q.question.lower())

    def test_do_to_mytestx(self):
        with io.open('tests/do/g100_do_pic.txt', encoding='cp1251') as f:
            self.assertEqual(f.read(), testparser.to_mytestx(self.quiz_do))


class TestMytestx(unittest.TestCase):
    def setUp(self):
        self.quiz_mytestx = testparser.parse_mytestx("tests/mytestx/quiz_sorted.txt")
        self.quiz_mytestx.sort(key=lambda q: q.question.lower())

        # Case with equal questions but different answers
        # Similar questions for shortener test
        self.quiz_mytestx_guileful = list(set(testparser.parse_mytestx("tests/mytestx/quiz_guileful.txt")))
        self.quiz_mytestx_guileful.sort(key=lambda q: q.question.lower())

    def test_mytestx_parser(self):
        mytestx = testparser.parse_mytestx("tests/mytestx/quiz_unsorted.txt")
        self.assertEqual(set(self.quiz_mytestx), set(mytestx))

    def test_mytestx_parser_duplicates(self):
        mytestx = testparser.parse_mytestx("tests/mytestx/quiz_unsorted_duplicates.txt")
        self.assertEqual(set(self.quiz_mytestx), set(mytestx))

        # Assertion make sense only if total questions > 1
        self.assertNotEqual(
            sorted(list(set(self.quiz_mytestx)),
                key=lambda q: q.question.lower()),
            sorted(list(set(mytestx)),
                key=lambda q: q.question.lower(), reverse=True))

    def test_to_mytestx_output(self):
        with io.open('tests/mytestx/quiz_sorted.txt', encoding='cp1251') as f:
            self.assertEqual(f.read(), testparser.to_mytestx(self.quiz_mytestx))


    def test_mytestx_to_mytestx_output(self):
        with io.open('tests/mytestx/quiz_guileful_mytestx.txt', encoding='cp1251') as f:
            self.assertEqual(f.read(), testparser.to_mytestx(self.quiz_mytestx_guileful))

    def test_mytestx_to_anki_output(self):
        with io.open('tests/mytestx/quiz_guileful_anki.csv') as f:
            self.assertEqual(f.read(), testparser.to_anki(self.quiz_mytestx_guileful))

    def test_mytestx_to_crib_output(self):
        with io.open('tests/mytestx/quiz_guileful_crib.txt') as f:
            self.assertEqual(f.read(), testparser.to_crib(self.quiz_mytestx_guileful))


if __name__ == '__main__':
    unittest.main()
