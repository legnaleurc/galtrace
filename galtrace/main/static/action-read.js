$( function() {

	$( '.dropdown-menu form' ).click( function( event ) {
		event.stopPropagation();
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
	function update() {
		Cart.view.updateFilter();
	}
	$( '#phase-filter' ).change( update );
	var previous = $( '#search' ).text();
	$( '#search' ).keyup( function( event ) {
		var current = $( this ).val();
		if( previous != current ) {
			previous = current;
			update();
		}
	} );
	// set initial filter
	$( '#phase-filter' ).val( [ 0 ] ).change();

	// NOTE: jQuery UI dialog module has a bug which causes Chrome gives an ignorable error. (#7293)

//	var cseDialog = $( '#search-dialog' ).modal();
	// Google CSE
	var customSearchControl = new google.search.CustomSearchControl( '006869288663536695394:98h-trd0op0' );
	customSearchControl.setResultSetSize( google.search.Search.FILTERED_CSE_RESULTSET );
	customSearchControl.draw( 'cse' );
	Cart.googleSearch = function( keyword ) {
		cseDialog.modal( 'show' );
		customSearchControl.execute( keyword );
	};

} );

// Google CSE
google.load( 'search', '1', {
	language : 'en'
} );
