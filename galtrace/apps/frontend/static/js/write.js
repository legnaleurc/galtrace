( function() {
	// insert dialog
	$( '#stdin button[type=submit]' ).click( function( event ) {
		event.preventDefault();

		var args = {
			title: GalTrace.makeSafe( $( '#id_title' ).val() ),
			uri: GalTrace.makeSafe( $( '#id_uri' ).val() ),
			date: $( '#id_date' ).val(),
			phase: parseInt( $( '#id_phase' ).val(), 10 ),
			vendor: GalTrace.makeSafe( $( '#id_vendor' ).val() ),
			volume: parseInt( $( '#id_volume' ).val(), 10 ),
			thumb: GalTrace.makeSafe( $( '#id_thumb' ).val() ),
		};
		if( args.title.length <= 0 || args.uri.length <= 0 ) {
			GalTrace.cerr( 'Field Error', 'No empty field(s)' );
			return false;
		}
		if( !/^\d\d\d\d\/\d\d\/\d\d$/.test( args.date ) ) {
			GalTrace.cerr( 'Date Format Error', 'e.g. 2011/11/02' );
			return false;
		}

		var self = $( this ).button( 'loading' );
		GalTrace.addOrder( args ).complete( function() {
			self.button( 'reset' );
		} ).done( function( data, textStatus, jqXHR ) {
			if( !data.success ) {
				GalTrace.cerr( data.type, data.message );
				return;
			}
			// clear input fields
			$( '#stdin input[type=text]' ).val( '' );
		} ).fail( function( jqXHR, textStatus, message ) {
			GalTrace.cerr( 'Unknown Error', message );
		} );
	} );
	// fetch dialog
	$( '#fetch' ).click( function( event ) {
		event.preventDefault();

		var uri = $( '#id_uri' ).val();
		if( uri === '' ) {
			return;
		}
		$( '#fetch' ).button( 'loading' );
		jQuery.post( GalTrace.urls.FETCH, {
			uri: uri
		}, null, 'json' ).always( function( jqXHR, textStatus ) {
			$( '#fetch' ).button( 'reset' );
		} ).done( function( data, textStatus, jqXHR ) {
			if( !data.success ) {
				GalTrace.cerr( data.type, data.message );
				return;
			}
			data = data.data;
			$( '#id_title' ).val( data.title );
			$( '#id_vendor' ).val( data.vendor );
			$( '#id_date' ).val( data.date );
			$( '#id_thumb' ).val( data.thumb );
		} ).fail( function( jqXHR, textStatus, message ) {
			GalTrace.cerr( 'Unknown Error', message );
		} );
	} );

	// edit dialog
	$( '#edit-modal button[type=submit]' ).click( function( event ) {s
		event.preventDefault();

		var args = {
			title: GalTrace.makeSafe( $( '#id_edit_title' ).val() ),
			uri: GalTrace.makeSafe( $( '#id_edit_uri' ).val() ),
			date: $( '#id_date' ).val(),
			vendor: GalTrace.makeSafe( $( '#id_edit_vendor' ).val() ),
			thumb: GalTrace.makeSafe( $( '#id_edit_thumb' ).val() ),
		};
		if( args.title.length <= 0 || args.uri.length <= 0 ) {
			GalTrace.cerr( 'Field Error', 'No empty field(s)' );
			return false;
		}
		if( !/^\d\d\d\d\/\d\d\/\d\d$/.test( args.date ) ) {
			GalTrace.cerr( 'Date Format Error', 'e.g. 2011/11/02' );
			return false;
		}

		var self = $( this ).button( 'loading' );
		GalTrace.editOrder( args ).complete( function() {
			self.button( 'reset' );
		} ).done( function( data, textStatus, jqXHR ) {
			if( !data.success ) {
				GalTrace.cerr( data.type, data.message );
				return;
			}
			// clear input fields
			$( '#edit-modal input[type=text]' ).val( '' );
		} ).fail( function( jqXHR, textStatus, message ) {
			GalTrace.cerr( 'Unknown Error', message );
		} );
	} );
	// update dialog
	$( '#update' ).click( function( event ) {
		event.preventDefault();

		var uri = $( '#id_edit_uri' ).val();
		if( uri === '' ) {
			return;
		}
		var self = $( this ).button( 'loading' );
		jQuery.post( GalTrace.urls.FETCH, {
			uri: uri
		}, null, 'json' ).always( function( jqXHR, textStatus ) {
			self.button( 'reset' );
		} ).done( function( data, textStatus, jqXHR ) {
			if( !data.success ) {
				GalTrace.cerr( data.type, data.message );
				return;
			}
			data = data.data;
			$( '#id_edit_title' ).val( data.title );
			$( '#id_edit_vendor' ).val( data.vendor );
			$( '#id_edit_date' ).val( data.date );
			$( '#id_edit_thumb' ).val( data.thumb );
		} ).fail( function( jqXHR, textStatus, message ) {
			GalTrace.cerr( 'Unknown Error', message );
		} );
	} );


	// move phase event
	$( '#control-panel a' ).click( function( event ) {
		event.preventDefault();

		var phase = $( this ).data( 'phase' );
		GalTrace.movePhase( phase ).done( function( data, textStatus, jqXHR ) {
			if( !data.success ) {
				GalTrace.cerr( data.type, data.message );
				return;
			}
		} ).error( function( jqXHR, textStatus, message ) {
			GalTrace.cerr( 'Unknown Error', message );
		} );
	} );

	// delete button
	$( '#button-delete' ).click( function( event ) {
		event.preventDefault();

		GalTrace.deleteOrders().done( function( data, textStatus, jqXHR ) {
			if( !data.success ) {
				GalTrace.cerr( data.type, data.message );
				return;
			}
		} ).error( function( jqXHR, textStatus, message ) {
			GalTrace.cerr( 'Unknown Error', message );
		} );
	} );
} )();
