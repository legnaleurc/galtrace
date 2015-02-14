#-*- coding: utf-8 -*-

import unittest

from galtrace.libs import crawler


class SiteTest(unittest.TestCase):

    def testGetchu(self):
        result = crawler.fetch('http://www.getchu.com/soft.phtml?id=614805')
        self.assertEqual(result['date'], '2009/06/26')
        self.assertEqual(result['title'], '鬼うた。')
        self.assertEqual(result['vendor'], '130cm')
        self.assertEqual(result['thumb'], 'http://www.getchu.com/./brandnew/614805/c614805package.jpg')

    def testDLsite(self):
        result = crawler.fetch('http://www.dlsite.com/pro/work/=/product_id/VJ006445.html')
        self.assertEqual(result['date'], '2011/12/02')
        self.assertEqual(result['title'], 'ヴァニタスの羊')
        self.assertEqual(result['vendor'], 'RococoWorks')
        self.assertEqual(result['thumb'], 'http://img.dlsite.jp/modpub/images2/work/professional/VJ007000/VJ006445_img_main.jpg')

    def testGyutto(self):
        result = crawler.fetch('http://gyutto.com/i/item74230')
        self.assertEqual(result['date'], '2012/01/27')
        self.assertEqual(result['title'], '嘘と真琴にお仕置きを')
        self.assertEqual(result['vendor'], '10mile')
        self.assertEqual(result['thumb'], 'http://gyutto.com/data/item_img/742/74230/74230.jpg')

    def testGyutto2(self):
        result = crawler.fetch('http://gyutto.com/i/item58146')
        self.assertEqual(result['date'], '2011/05/03')
        self.assertEqual(result['title'], '生徒会長で甘えん坊なお姉ちゃんは好きですか？')
        self.assertEqual(result['vendor'], 'アルトワークス')
        self.assertEqual(result['thumb'], 'http://gyutto.com/data/item_img/581/58146/58146.jpg')

    def testDLGetchuDoujin(self):
        result = crawler.fetch('http://dl.getchu.com/index.php?action=gd&gcd=D0006562&cirid=72&cp=&c=')
        self.assertEqual(result['date'], '2009/07/24')
        self.assertEqual(result['title'], 'Tentacle and Witches')
        self.assertEqual(result['vendor'], 'Lilith / PIXY / ZIZ')
        self.assertEqual(result['thumb'], 'http://dl.getchu.com/images/circle/72/6562GOODS_IMAGE_MAINApp.jpg')

    def testDLGetchuShougyou(self):
        result = crawler.fetch('http://dl.getchu.com/index.php?action=gdSoft&gcd=74749&cp=&c=')
        self.assertEqual(result['date'], '2012/02/24')
        self.assertEqual(result['title'], 'めちゃ婚！')
        self.assertEqual(result['vendor'], 'onomatope*')
        self.assertEqual(result['thumb'], 'http://dl.getchu.com/images/soft/74749/74749large.jpg')

if __name__ == '__main__':
    unittest.main()
