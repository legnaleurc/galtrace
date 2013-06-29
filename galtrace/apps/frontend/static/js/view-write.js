var GalTrace = GalTrace || {};
(function () {
	'use strict';

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
}());
