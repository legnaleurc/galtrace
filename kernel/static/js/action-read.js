( function() {

	// create table and load orders
	GalTrace.initialize( '#orders' );

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
	$( 'a[rel=external]' ).click( function( event ) {
		event.preventDefault();
		window.open( $( this ).attr( 'href' ), '_blank' );
	} );

	// apply filter
	$( '.phase-filter' ).click( function( event ) {
		event.preventDefault();
		var self = $( this );
		self.toggleClass( 'active' );
		GalTrace.emit( 'GalTrace.phaseChanged', [ self.data( 'value' ), self.hasClass( 'active' ) ] );
	} );
	var previous = $( '#search' ).text();
	$( '#search' ).keyup( function( event ) {
		var current = $( this ).val();
		if( previous !== current ) {
			GalTrace.emit( 'GalTrace.searchChanged', [ current, current.indexOf( previous ) < 0 && previous.indexOf( current ) < 0, current.length > previous.length ] );
			previous = current;
		}
	} );
	// set initial filter
	$( '.phase-filter[data-value="0"]' ).click();

	var cseDialog = $( '#search-modal' ).modal( {
		show: false
	} );
	// Google CSE
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

} )();
