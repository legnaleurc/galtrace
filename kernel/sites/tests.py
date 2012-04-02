#-*- coding: utf-8 -*-

from kernel import sites

import unittest

class SiteTest( unittest.TestCase ):

	def testGetchu( self ):
		result = sites.fetch( 'http://www.getchu.com/soft.phtml?id=614805' )
		self.assertEqual( result['date'], '2009/06/26' )
		self.assertEqual( result['title'], u'鬼うた。' )
		self.assertEqual( result['vendor'], '130cm' )

	def testDLsite( self ):
		result = sites.fetch( 'http://www.dlsite.com/pro/work/=/product_id/VJ006445.html' )
		self.assertEqual( result['date'], '2011/12/02' )
		self.assertEqual( result['title'], u'ヴァニタスの羊' )
		self.assertEqual( result['vendor'], 'RococoWorks' )

	def testGyutto( self ):
		result = sites.fetch( 'http://gyutto.com/i/item74230' )
		self.assertEqual( result['date'], '2012/01/27' )
		self.assertEqual( result['title'], u'嘘と真琴にお仕置きを' )
		self.assertEqual( result['vendor'], '10mile' )

	def testDLGetchu1( self ):
		result = sites.fetch( 'http://dl.getchu.com/index.php?action=gd&gcd=D0006562&cirid=72&cp=&c=' )
		self.assertEqual( result['date'], '2009/07/24' )
		self.assertEqual( result['title'], 'Tentacle and Witches' )
		self.assertEqual( result['vendor'], 'Lilith / Pixy' )

	@unittest.expectedFailure
	def testDLGetchu2( self ):
		result = sites.fetch( 'http://dl.getchu.com/index.php?action=gdSoft&gcd=74749&cp=&c=' )
		self.assertEqual( result['date'], '2012/02/24' )
		self.assertEqual( result['title'], u'めちゃ婚！' )
		self.assertEqual( result['vendor'], 'onomatope*' )

if __name__ == '__main__':
	unittest.main()
