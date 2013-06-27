var GalTrace = GalTrace || {};
( function() {
	'use strict';

	GalTrace.saveOrder = function( args ) {
		// send request, server will handle INSERT/UPDATE by itself
		var request = jQuery.post( GalTrace.urls.SAVE, args, null, 'json' );

		// find if exists (by title); can not use binary search here
		var model = GalTrace.orderList.find( function( model_ ) {
			return model_.get( 'title' ) === args.title;
		} );
		// only update data and move order if success
		if( model !== undefined ) {
			model.set( 'updating', true );
			return request.done( function( data ) {
				// update data and HTML
				if( !data.success ) {
					GalTrace.cerr( data.type, data.message );
					return;
				}
				data = data.data;
				model.set( {
					title: data.title,
					vendor: data.vendor,
					date: data.date,
					uri: data.uri,
					thumb: data.thumb,
					phase: data.phase,
					volume: data.volume,
					updating: false,
				} );
				GalTrace.orderList.sort();
			} );
		}

		return request.done( function( data ) {
			if( !data.success ) {
				GalTrace.cerr( data.type, data.message );
				return;
			}
			var model = new GalTrace.Order( data.data );
			GalTrace.orderList.add( model );
			// NOTE force update
			model.set( 'updating', true );
			model.set( 'updating', false );
		} );
	};

	GalTrace.movePhase = function( phase ) {
		var selected = GalTrace.orderList.filter( function( model ) {
			return model.get( 'selected' );
		} );
		_.each( selected, function( model ) {
			model.set( 'updating', true );
		} );
		var request = jQuery.post( GalTrace.urls.MOVE, {
			phase: phase,
			orders: _.map( selected, function( value ) {
				return value.get( 'title' );
			} ),
		}, null, 'json' ).done( function() {
			_.each( selected, function( element ) {
				element.set( {
					phase: phase,
					selected: false,
				} );
			} );
		} ).always( function() {
			_.each( selected, function( model ) {
				model.set( 'updating', false );
			} );
		} );
		return request;
	};

	GalTrace.deleteOrders = function() {
		var selected = GalTrace.orderList.filter( function( model ) {
			return model.get( 'selected' );
		} );
		var request = jQuery.post( GalTrace.urls.DELETE, {
			orders: _.map( selected, function( value ) {
				return value.get( 'title' );
			} ),
		}, null, 'json' ).done( function() {
			GalTrace.orderList.remove( selected );
		} );
		return request;
	};

	GalTrace.makeSafe = function( unsafe ) {
		return $( jQuery.parseHTML( unsafe ) ).text();
	};

	// select action
	$( '#orders' ).on( 'click', '.check-btn', function() {
		var self = $( this );
		self.toggleClass( 'checked' );
		var model = GalTrace.orderList.get( self.parent().data( 'cid' ) );
		model.set( 'selected', self.hasClass( 'checked' ), {
			silent: true,
		} );
	} );

	// edit action
	$( '#orders' ).on( 'click', '.edit-btn', function() {
		var model = GalTrace.orderList.get( $( this ).parent().data( 'cid' ) );
		GalTrace.editDialog.modal( 'toggle' );
		$( '#id_edit_title' ).val( model.get( 'title' ) );
		$( '#id_edit_title' ).data( 'title', model.get( 'title' ) );
		$( '#id_edit_vendor' ).val( model.get( 'vendor' ) );
		$( '#id_edit_date' ).val( model.get( 'date' ) );
		$( '#id_edit_uri' ).val( model.get( 'uri' ) );
	} );

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
		GalTrace.saveOrder( args ).complete( function() {
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
	$( '#edit-modal button[type=submit]' ).click( function( event ) {
		event.preventDefault();

		var args = {
			title: GalTrace.makeSafe( $( '#id_edit_title' ).data( 'title' ) ),
			uri: GalTrace.makeSafe( $( '#id_edit_uri' ).val() ),
			date: $( '#id_edit_date' ).val(),
			vendor: GalTrace.makeSafe( $( '#id_edit_vendor' ).val() ),
			thumb: GalTrace.makeSafe( $( '#id_edit_thumb' ).val() ),
		};
		if( args.title.length <= 0 || args.uri.length <= 0 ) {
			GalTrace.cerr( 'Field Error', 'No empty field(s)' );
			return false;
		}
		if( $( '#id_edit_title' ).val() !== args.title ) {
			args.new_title = $( '#id_edit_title' ).val();
		}
		if( !/^\d\d\d\d\/\d\d\/\d\d$/.test( args.date ) ) {
			GalTrace.cerr( 'Date Format Error', 'e.g. 2011/11/02' );
			return false;
		}

		var self = $( this ).button( 'loading' );
		GalTrace.saveOrder( args ).complete( function() {
			self.button( 'reset' );
		} ).done( function( data, textStatus, jqXHR ) {
			if( !data.success ) {
				GalTrace.cerr( data.type, data.message );
				return;
			}
			// clear input fields
			$( '#edit-modal input[type=text]' ).val( '' );
			GalTrace.editDialog.modal( 'toggle' );
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
