"""
Tests for appstats module
"""

import unittest
from pygame_utils import AppStats, AppStat


class TestAppStat(unittest.TestCase):
    def test_initialization(self):
        stat = AppStat('test', 10)
        self.assertEqual(stat.name, 'test')
        self.assertEqual(stat.value, 10)
        self.assertEqual(stat.total_samples, 1)
        self.assertEqual(stat.mean, 10)
        self.assertEqual(stat.min, 10)
        self.assertEqual(stat.max, 10)

    def test_sampling(self):
        stat = AppStat('test', 10)
        stat.sample(20)
        stat.sample(15)
        
        self.assertEqual(stat.value, 15)
        self.assertEqual(stat.total_samples, 3)
        self.assertEqual(stat.min, 10)
        self.assertEqual(stat.max, 20)
        self.assertGreater(stat.mean, 10)
        self.assertLess(stat.mean, 20)

    def test_reset(self):
        stat = AppStat('test', 10)
        stat.sample(20)
        stat.reset()
        
        self.assertEqual(stat.value, 0)
        self.assertEqual(stat.total_samples, 0)
        self.assertEqual(stat.mean, 0)
        self.assertEqual(stat.min, 0)
        self.assertEqual(stat.max, 0)


class TestAppStats(unittest.TestCase):
    def setUp(self):
        # Clear stats before each test
        AppStats.items.clear()

    def test_sample_creates_new_stat(self):
        stat = AppStats.sample('test', 10)
        self.assertIsInstance(stat, AppStat)
        self.assertEqual(stat.value, 10)

    def test_sample_updates_existing_stat(self):
        AppStats.sample('test', 10)
        stat = AppStats.sample('test', 20)
        self.assertEqual(stat.total_samples, 2)
        self.assertEqual(stat.value, 20)

    def test_get_single_stat(self):
        AppStats.sample('test', 10)
        stat = AppStats.get('test')
        self.assertIsInstance(stat, AppStat)
        self.assertEqual(stat.name, 'test')

    def test_get_all_stats(self):
        AppStats.sample('stat1', 10)
        AppStats.sample('stat2', 20)
        all_stats = AppStats.get()
        self.assertIsInstance(all_stats, dict)
        self.assertEqual(len(all_stats), 2)
        self.assertIn('stat1', all_stats)
        self.assertIn('stat2', all_stats)


if __name__ == '__main__':
    unittest.main()

