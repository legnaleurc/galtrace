( function() {

	// create table
	Cart.view = new Cart.Table( '#cart' );

	// load orders, tail recursion
	function load() {
		jQuery.post( '/load.cgi', {
			offset: Cart.view.size(),
			limit: 100,
		}, null, 'json' ).success( function( data, textStatus, jqXHR ) {
			if( !data.success ) {
				Cart.cerr( data.type, data.message );
				return;
			}
			if( data.data === null ) {
				// stop
				return;
			}

			load();

			$( data.data ).each( function() {
				Cart.view.append( new Cart.DynamicRow( this ) );
			} );
		} ).error( function( jqXHR, textStatus, message ) {
			Cart.cerr( 'Unknown Error', message );
		} );
	}
	load();

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
	function update() {
		Cart.view.updateFilter();
	}
	$( '.phase-filter' ).click( function( event ) {
		event.preventDefault();
		$( this ).toggleClass( 'active' );
		update();
	} );
	var previous = $( '#search' ).text();
	$( '#search' ).keyup( function( event ) {
		var current = $( this ).val();
		if( previous != current ) {
			previous = current;
			update();
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
			Cart.googleSearch = function( keyword ) {
				cseDialog.modal( 'show' );
				customSearchControl.execute( keyword );
			};
		},
	} );

} )();
