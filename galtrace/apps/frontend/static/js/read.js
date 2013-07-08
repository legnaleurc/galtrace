var GalTrace = GalTrace || {};
( function() {
	'use strict';

	GalTrace.userID = location.pathname.match( /^\/([\w_]+).*$/ )[1];

	GalTrace.cerr = function( type, message ) {
		console.error( [ type, ': ', message ].join( '' ) );
	};

	GalTrace.load = function( phase ) {
		function load( offset ) {
			jQuery.post( GalTrace.urls.LOAD, {
				offset: offset,
				limit: 100,
				phase: phase,
				user_id: GalTrace.userID,
			}, null, 'json' ).done( function( data, textStatus, jqXHR ) {
				if( !data.success ) {
					GalTrace.cerr( data.type, data.message );
					return;
				}
				if( data.data === null ) {
					// load finished
					return;
				}
				data = data.data;

				load( offset + data.length );

				GalTrace.orderList.add( data );
			} ).fail( function( jqXHR, textStatus, message ) {
				GalTrace.cerr( 'Unknown Error', message );
			} );
		}

		load( 0 );
	};

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

	// search action
	$( '#orders' ).on( 'click', '.search-btn', function() {
		GalTrace.googleSearch( GalTrace.orderList.get( $( this ).parent().data( 'cid' ) ).get( 'title' ) );
	} );

	// alert widget
	$( '#stderr .close' ).click( function( event ) {
		event.preventDefault();

		$( '#stderr' ).fadeOut( 'slow' );
	} );

	// open in new window/tab
	$( document.body ).on( 'click', 'a[rel="external"]', function( event ) {
		event.preventDefault();
		window.open( $( this ).attr( 'href' ), '_blank' );
	} );

} )();
