var GalTrace = GalTrace || {};
( function() {
	'use strict';

	var ORDER_TEMPLATE = _.template( $( '#order-template' ).html() );

	var COUNTER_TEMPLATE = _.template( $( '#counter-template' ).html() );

	var OrderView = Backbone.View.extend( {
		tagName: 'tr',

		initialize: function() {
			this.model.on( 'change:vendor', this.onVendorChanged, this );
			this.model.on( 'change:date', this.onDateChanged, this );
			this.model.on( 'change:uri', this.onUriChanged, this );
			this.model.on( 'change:phase', this.onFilterChanged, this );
			this.model.on( 'change:selected', this.onSelectionChanged, this );
			this.model.on( 'change:updating', this.onStateChanged, this );
			GalTrace.orderFilter.on( 'change:phases change:search', this.onFilterChanged, this );

			// bookkeeping
			this.$el.data( 'view', this );
		},

		render: function() {
			var title = this.model.get( 'title' );
			var vendor = this.model.get( 'vendor' );
			var date = this.model.get( 'date' );
			var uri = this.model.get( 'uri' );

			var template = ORDER_TEMPLATE( {
				title: title,
				vendor: vendor,
				date: date,
				uri: uri,
			} );
			this.$el.html( template );

			this.$( '.check' ).change( GalTrace.bind( function( model_ ) {
				model_.set( 'selected', $( this ).is( ':checked' ), {
					silent: true,
				} );
			}, this.model ) );

			this.$( '.search' ).click( function( event ) {
				event.preventDefault();
				GalTrace.googleSearch( title );
			} );

			function makeEditor( opts ) {
				var $B = GalTrace.bind;
				var label = opts.cell.children( 'span.inline-label' );
				var edit = opts.cell.children( 'input.inline-edit' );
				opts.cell.dblclick( function() {
					opts.cell.addClass( 'editing' );
					edit.focus();
				} );
				function onFinished() {
					var labelText = label.text();
					var inputText = edit.val();
					if( labelText !== inputText && ( opts.validator ? opts.validator( inputText ) : true ) ) {
						var args = {
							title: opts.orderKey,
						};
						args[opts.fieldKey] = inputText;
						jQuery.post( GalTrace.urls.SAVE, args, null, 'json' ).success( function( data, textStatus, jqXHR ) {
							if( !data.success ) {
								// TODO display error message
								return;
							}
							opts.model.set( opts.fieldKey, inputText );
							GalTrace.orderList.sort();
						} );
					}
					opts.cell.removeClass( 'editing' );
				}
				edit.blur( onFinished ).keypress( function( event ) {
					if( event.which === 13 ) {
						onFinished();
					}
				} );
			}

			// vendor cell
			makeEditor( {
				cell: this.$( '.vendor' ),
				validator: null,
				model: this.model,
				orderKey: title,
				fieldKey: 'vendor',
			} );

			// date cell
			makeEditor( {
				cell: this.$( '.date' ),
				validator: function( inputText ) {
					return /^\d\d\d\d\/\d\d\/\d\d$/.test( inputText );
				},
				model: this.model,
				orderKey: title,
				fieldKey: 'date',
			} );

			var phases = GalTrace.orderFilter.get( 'phases' );
			var search = GalTrace.orderFilter.get( 'search' ).toLowerCase();
			var phase = this.model.get( 'phase' );
			if( !phases[phase] || ( title.toLowerCase().indexOf( search ) < 0 && vendor.toLowerCase().indexOf( search ) < 0 ) ) {
				this.$el.css( {
					display: 'none',
				} );
			}

			return this;
		},

		onVendorChanged: function() {
			var vendor = this.model.get( 'vendor' );
			this.$( 'td.vendor span.inline-label' ).attr( {
				title: vendor,
			} ).text( vendor );
		},

		onDateChanged: function() {
			this.$( 'td.date span.inline-label' ).text( this.model.get( 'date' ) );
		},

		onUriChanged: function() {
			this.$( '.uri' ).attr( {
				href: this.model.get( 'uri' ),
			} );
		},

		onFilterChanged: function() {
			var search = GalTrace.orderFilter.get( 'search' ).toLowerCase();
			var title = this.model.get( 'title' ).toLowerCase();
			var vendor = this.model.get( 'vendor' ).toLowerCase();
			if( GalTrace.orderFilter.get( 'phases' )[this.model.get( 'phase' )] && ( title.indexOf( search ) >= 0 || vendor.indexOf( search ) >= 0 ) ) {
				this.$el.css( {
					display: 'table-row',
				} );
			} else {
				this.$el.css( {
					display: 'none',
				} );
			}
		},

		onSelectionChanged: function() {
			this.$( '.check' ).attr( {
				checked: this.model.get( 'selected' ),
			} );
		},

		onStateChanged: function() {
			var updating = this.model.get( 'updating' );
			if( updating ) {
				this.$el.removeClass( 'success error' ).addClass( 'info' );
			} else {
				var tmp = window.innerHeight / 2;
				$( 'html, body' ).animate( {
					scrollTop: this.$el.offset().top - tmp,
				}, 1000 );
				this.$el.removeClass( 'info' ).addClass( 'success' );
				tmp = this.$el;
				var handle = setTimeout( function() {
					tmp.removeClass( 'success' );
				}, 5000 );
			}
		},
	} );

	var OrderListView = Backbone.View.extend( {
		initialize: function() {
			this.model.on( 'add', this.onAdd, this );
			this.model.on( 'remove', this.onRemove, this );
			this.model.on( 'reset', this.reRender, this );
		},

		onAdd: function( model_, self, options ) {
			var view = new OrderView( {
				model: model_,
			} );
			var children = this.$el.children();
			if( children.length === 0 ) {
				// first but empty
				this.$el.append( view.$el );
			} else if( options.index === children.length ) {
				// last
				children.last().after( view.$el );
			} else if( options.index > 0 ) {
				// middle
				$( children[options.index] ).before( view.$el );
			} else {
				// first
				children.first().before( view.$el );
			}
			view.render();
		},

		onRemove: function( model_, self, options ) {
			$( this.$el.children()[options.index] ).remove();
		},

		reRender: function() {
			var els = this.$el.children().detach();
			els.sort( function( l, r ) {
				l = this.model.indexOf( $( l ).data( 'view' ).model );
				r = this.model.indexOf( $( r ).data( 'view' ).model );
				if( l === r ) {
					return 0;
				}
				return ( l < r ) ? -1 : 1;
			}.bind( this ) );
			els.each( function( index, element ) {
				this.$el.append( element );
			}.bind( this ) );
		},
	} );

	var CounterView = Backbone.View.extend( {
		initialize: function() {
			this.model.on( 'add', this.onAdd, this );
			this.model.on( 'remove', this.onRemove, this );
			GalTrace.orderFilter.on( 'change:phases change:search', this.onFilterChanged, this );

			this.render();
		},

		render: function() {
			var total = this.model.length;
			var phases = GalTrace.orderFilter.get( 'phases' );
			var count = this.model.filter( function( model ) {
				return phases[model.get( 'phase' )];
			} ).length;
			var template = COUNTER_TEMPLATE( {
				total: total,
				current: count,
			} );
			this.$el.html( template );
		},

		onAdd: function( model_ ) {
			model_.on( 'change:phase', this.onModelPhaseChange, this );
			if( GalTrace.orderFilter.get( 'phases' )[model_.get( 'phase' )] ) {
				var tmp = $( '#current-orders' );
				tmp.text( parseInt( tmp.text(), 10 ) + 1 );
			}
			$( '#total-orders' ).text( this.model.length );
		},

		onRemove: function( model_ ) {
			if( GalTrace.orderFilter.get( 'phases' )[model_.get( 'phase' )] ) {
				var tmp = $( '#current-orders' );
				tmp.text( parseInt( tmp.text(), 10 ) - 1 );
			}
			$( '#total-orders' ).text( this.model.length );
		},

		onFilterChanged: function() {
			var phases = GalTrace.orderFilter.get( 'phases' );
			var count = this.model.filter( function( model ) {
				return phases[model.get( 'phase' )];
			} ).length;
			var tmp = $( '#current-orders' );
			tmp.text( count );
		},

		onModelPhaseChange: function( model_, value ) {
			var tmp = $( '#current-orders' );
			if( GalTrace.orderFilter.get( 'phases' )[value] ) {
				tmp.text( parseInt( tmp.text(), 10 ) + 1 );
			} else {
				tmp.text( parseInt( tmp.text(), 10 ) - 1 );
			}
		},
	} );

	var orderListView = new OrderListView( {
		el: '#orders',
		model: GalTrace.orderList,
	} );
	var counterView = new CounterView( {
		el: '#counter',
		model: GalTrace.orderList,
	} );
} )();
