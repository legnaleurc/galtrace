( function() {
	'use strict';

	// create table and load orders
	GalTrace.initialize();

	$( document ).bind( 'pageinit', function() {
		$( 'a.phase-filter[data-value=0]' ).click();
	} );
} )();
