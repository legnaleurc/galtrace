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

	function EditorDialog( selector ) {
		var dialog = $( selector ).modal( {
			show: false,
		} );
		var __ = {
			dialog: dialog,
			fields: {
				title: {
					element: dialog.find( 'input[name=title]' ),
					validate: function( context ) {
						var old = this.element.data( 'title' );
						old = GalTrace.makeSafe( old );
						var new_ = this.element.val();
						new_ = GalTrace.makeSafe( new_ );
						if( old.length <= 0 || new_.length <= 0 ) {
							throw new Error( 'title should not be empty' );
						}
						context.title = old;
						if( new_ !== old ) {
							context.new_title = new_;
						}
					},
				},
				uri: {
					element: dialog.find( 'input[name=uri]' ),
					validate: function( context ) {
						var uri = this.element.val();
						uri = GalTrace.makeSafe( uri );
						if( uri.length <= 0 ) {
							throw new Error( 'uri should not be empty' );
						}
						context.uri = uri;
					},
				},
				date: {
					element: dialog.find( 'input[name=date]' ),
					validate: function( context ) {
						var date = this.element.val();
						if( !/^\d\d\d\d\/\d\d\/\d\d$/.test( date ) ) {
							throw new Error( 'date format error (e.g. 2011/11/02)' );
						}
						context.date = date;
					},
				},
				vendor: {
					element: dialog.find( 'input[name=vendor]' ),
					validate: function( context ) {
						var vendor = this.element.val();
						vendor = GalTrace.makeSafe( vendor );
						if( vendor.length <= 0 ) {
							throw new Error( 'vendor should not be empty' );
						}
						context.vendor = vendor;
					},
				},
				thumb: {
					element: dialog.find( 'input[name=thumb]' ),
					validate: function( context ) {
						var thumb = this.element.val();
						context.thumb = thumb;
					},
				},
			},
			submit: dialog.find( 'button[type=submit]' ),
			reset: dialog.find( 'button[type=reset]' ),
			update: dialog.find( 'button[type=button]' ),
		};
		this._ = __;

		function getArgs() {
			var args = {};
			_.each( __.fields, function( field ) {
				field.validate( args );
			} );
			return args;
		}


		__.submit.click( function( event ) {
			event.preventDefault();

			try {
				var args = getArgs();
			} catch ( e ) {
				GalTrace.cerr( 'Invalid Field(s)', e.message );
				return;
			}
			var self = __.submit.button( 'loading' );

			GalTrace.saveOrder( args ).complete( function() {
				self.button( 'reset' );
			} ).done( function( data, textStatus, jqXHR ) {
				if( !data.success ) {
					GalTrace.cerr( data.type, data.message );
					return;
				}
				GalTrace.editor.hide();
			} ).fail( function( jqXHR, textStatus, message ) {
				GalTrace.cerr( 'Unknown Error', message );
			} );
		} );

		// update dialog
		__.update.click( function( event ) {
			event.preventDefault();

			var uri = __.fields.uri.element.val();
			if( !uri ) {
				return;
			}
			var self = __.update.button( 'loading' );
			jQuery.post( GalTrace.urls.FETCH, {
				uri: uri
			}, null, 'json' ).always( function() {
				self.button( 'reset' );
			} ).done( function( data, textStatus, jqXHR ) {
				if( !data.success ) {
					GalTrace.cerr( data.type, data.message );
					return;
				}
				data = data.data;
				__.fields.title.element.val( data.title );
				__.fields.vendor.element.val( data.vendor );
				__.fields.date.element.val( data.date );
				__.fields.thumb.element.val( data.thumb );
			} ).fail( function( jqXHR, textStatus, message ) {
				GalTrace.cerr( 'Unknown Error', message );
			} );
		} );
	}
	EditorDialog.prototype.show = function( cid ) {
		var model = GalTrace.orderList.get( cid );
		this._.dialog.modal( 'show' );
		this._.fields.title.element.val( model.get( 'title' ) );
		this._.fields.title.element.data( 'title', model.get( 'title' ) );
		this._.fields.vendor.element.val( model.get( 'vendor' ) );
		this._.fields.date.element.val( model.get( 'date' ) );
		this._.fields.uri.element.val( model.get( 'uri' ) );
	};
	EditorDialog.prototype.hide = function() {
		// clear input fields
		this._.reset.click();
		this._.dialog.modal( 'hide' );
	};
	GalTrace.editor = new EditorDialog( '#editor-modal' );

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
		var cid = $( this ).parent().data( 'cid' );
		GalTrace.editor.show( cid );
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
