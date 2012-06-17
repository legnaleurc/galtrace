( function() {

	// select all event
	$( '#select-all' ).change( function( event ) {
		$( '.check' ).attr( 'checked', $( this ).is( ':checked' ) );
	} );

	// delete button
	$( '#button-delete' ).click( function( event ) {
		event.preventDefault();

		for( var i = Cart.view.size() - 1; i >= 0; --i ) {
			if( Cart.view.at( i ).isChecked() ) {
				Cart.view.take( i ).remove().success( function( data, textStatus, jqXHR ) {
					if( !data.success ) {
						Cart.cerr( data.type, data.message );
					}
				} ).error( function( jqXHR, textStatus, message ) {
					Cart.cerr( 'Unknown Error', message );
				} );
			}
		}
	} );

	// move phase event
	$( '#control-panel a' ).click( function( event ) {
		event.preventDefault();

		var phase = $( this ).data( 'phase' );
		var visible = $( '.phase-filter[data-value="' + phase + '"]' ).hasClass( 'active' );
		for( var i = 0; i < Cart.view.size(); ++i ) {
			var row = Cart.view.at( i );
			// if not selected or phase no need to change, skip this part
			if( !row.isChecked() || phase === row.getPhase() ) {
				continue;
			}

			var currentOrders = $( '#current-orders' );
			var diff = parseInt( currentOrders.text(), 10 );
			// update phase and clear selection
			row.setPhase( phase ).setChecked( false );
			// update hidden state
			if( visible ) {
				++diff;
				row.getElement().show();
			} else {
				--diff;
				row.getElement().hide();
			}
			currentOrders.text( diff );
			// sync to database
			row.save().success( function( data, textStatus, jqXHR ) {
				if( !data.success ) {
					Cart.cerr( data.type, data.message );
					return;
				}
			} ).error( function( jqXHR, textStatus, message ) {
				Cart.cerr( 'Unknown Error', message );
			} );
		}
	} );

	// insert dialog
	$( '#fetch' ).click( function( event ) {
		event.preventDefault();

		var uri = $( '#id_uri' ).val();
		if( uri === '' ) {
			return;
		}
		jQuery.post( Cart.urls.FETCH, {
			uri: uri
		}, null, 'json' ).success( function( data, textStatus, jqXHR ) {
			if( !data.success ) {
				Cart.cerr( data.type, data.message );
				return;
			}
			data = data.data;
			$( '#id_title' ).val( data.title );
			$( '#id_vendor' ).val( data.vendor );
			$( '#id_date' ).val( data.date );
		} ).error( function( jqXHR, textStatus, message ) {
				Cart.cerr( 'Unknown Error', message );
		} );
	} );
	$( '#stdin button[type=submit]' ).click( function( event ) {
		event.preventDefault();

		var args = {
			title: $( '#id_title' ).val(),
			uri: $( '#id_uri' ).val(),
			date: $( '#id_date' ).val(),
			phase: parseInt( $( '#id_phase' ).val(), 10 ),
			vendor: $( '#id_vendor' ).val(),
			volume: parseInt( $( '#id_volume' ).val(), 10 )
		};
		if( args.title.length <= 0 || args.uri.length <= 0 ) {
			Cart.cerr( 'Field Error', 'No empty field(s)' );
			return false;
		}
		if( !/^\d\d\d\d\/\d\d\/\d\d$/.test( args.date ) ) {
			Cart.cerr( 'Date Format Error', 'e.g. 2011/11/02' );
			return false;
		}

		Cart.view.newRow( args ).success( function( data, textStatus, jqXHR ) {
			if( !data.success ) {
				Cart.cerr( data.type, data.message );
				return;
			}
			// clear input fields
			$( '#stdin input[type=text]' ).val( '' );
		} ).error( function( jqXHR, textStatus, message ) {
			Cart.cerr( 'Unknown Error', message );
		} );
	} );

} )();
