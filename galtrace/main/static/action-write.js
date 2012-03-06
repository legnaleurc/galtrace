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
				Cart.view.take( i ).remove();
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
			} else {
				// update phase and clear selection
				row.setPhase( phase ).setChecked( false );
				// update hidden state
				if( visible ) {
					row.getElement().show();
				} else {
					row.getElement().hide();
				}
				// sync to database
				row.save();
			}
		}
	} );

	// insert dialog
	$( '#fetch' ).click( function( event ) {
		event.preventDefault();

		var uri = $( '#id_uri' ).val();
		if( uri === '' ) {
			return;
		}
		jQuery.post( 'fetch.cgi', {
			uri: uri
		}, function( data, textStatus, message ) {
			if( textStatus !== 'success' ) {
				Cart.cerr( '#insert-modal .modal-footer', message );
				return;
			}
			if( data === null ) {
				Cart.cerr( '#insert-modal .modal-footer', 'Fetched nothing.' );
				return;
			}
			$( '#id_title' ).val( data.title );
			$( '#id_vendor' ).val( data.vendor );
			$( '#id_date' ).val( data.date );
		}, 'json' );
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
		if( args.title === '' || args.uri === '' ) {
			Cart.cerr( '#insert-modal .modal-footer', 'No empty field(s)' );
			return false;
		}
		if( !/^\d\d\d\d\/\d\d\/\d\d$/.test( args.date ) ) {
			Cart.cerr( '#insert-modal .modal-footer', 'Wrong date: ' + args.date );
			return false;
		}

		Cart.view.newRow( args, function() {
			// clear input fields
			$( '#stdin input[type=text]' ).val( '' );
		} );
	} );

} )();
