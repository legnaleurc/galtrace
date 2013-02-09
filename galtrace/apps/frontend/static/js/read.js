( function() {
	'use strict';

	// create table and load orders
	GalTrace.initialize();

	// apply filter
	$( '.phase-filter' ).click( function( event ) {
		event.preventDefault();
		var self = $( this );
		self.toggleClass( 'active' );
		var tmp = GalTrace.orderFilter.get( 'phases' );
		tmp[self.data( 'value' )] = self.hasClass( 'active' );
		GalTrace.orderFilter.set( 'phases', tmp );
		// FIXME somehow I must trigger this manually
		GalTrace.orderFilter.trigger( 'change:phases' );
	} );
	// set initial filter
	$( '.phase-filter[data-value="0"]' ).click();
	// search filter
	var previous = $( '#query-string' ).text();
	$( '#query-string' ).keyup( function( event ) {
		var current = $( this ).val();
		if( previous !== current ) {
			GalTrace.orderFilter.set( 'queryString', current );
			GalTrace.orderFilter.trigger( 'change:queryString' );
			previous = current;
		}
	} );

	// Google CSE
	var cseDialog = $( '#search-modal' ).modal( {
		show: false
	} );
	google.load( 'search', '1', {
		language: 'en',
		callback: function() {
			var customSearchControl = new google.search.CustomSearchControl( '006869288663536695394:98h-trd0op0' );
			customSearchControl.setResultSetSize( google.search.Search.FILTERED_CSE_RESULTSET );
			customSearchControl.draw( 'cse' );
			GalTrace.googleSearch = function( keyword ) {
				cseDialog.modal( 'show' );
				customSearchControl.execute( keyword );
			};
		},
	} );

	// alert widget
	$( '#stderr .close' ).click( function( event ) {
		event.preventDefault();

		$( '#stderr' ).fadeOut( 'slow' );
	} );

	// select all on click
	$( '#stdin input[type=text]' ).focus( function() {
		this.select();
	} );

	// open in new window/tab
	$( document.body ).on( 'click', 'a[rel="external"]', function( event ) {
		event.preventDefault();
		window.open( $( this ).attr( 'href' ), '_blank' );
	} );

} )();
