( function() {
	'use strict';

	// create table and load orders
	GalTrace.initialize();

	// apply filter
	$( '.phase-filter' ).click( function( event ) {
		event.preventDefault();
		var self = $( this );
		self.toggleClass( 'ui-btn-active' );
		var tmp = GalTrace.orderFilter.get( 'phases' );
		tmp[self.data( 'value' )] = self.hasClass( 'ui-btn-active' );
		GalTrace.orderFilter.set( 'phases', tmp );
		// FIXME somehow I must trigger this manually
		GalTrace.orderFilter.trigger( 'change:phases' );
		return false;
	} );
	// set initial filter
	$( '.phase-filter[data-value="0"]' ).click();
} )();
