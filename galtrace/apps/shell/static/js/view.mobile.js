var GalTrace = GalTrace || {};
( function() {
	'use strict';

	var ORDER_TEMPLATE = _.template( $( '#order-template' ).html() );

	var OrderView = Backbone.View.extend( {
		tagName: 'div',

		attributes: {
			'data-role': 'collapsible',
			'data-collapsed': true,
			'data-iconpos': 'right',
		},

		initialize: function() {
			this.model.on( 'change:vendor', this.onVendorChanged, this );
			this.model.on( 'change:date', this.onDateChanged, this );
			this.model.on( 'change:uri', this.onUriChanged, this );
			this.model.on( 'change:phase', this.onFilterChanged, this );
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
			this.$el.trigger( 'create' );
			this.$el.collapsible();

			this.$( '.search' ).click( function( event ) {
				event.preventDefault();
				GalTrace.googleSearch( title );
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
			this.$( '.vendor' ).text( this.model.get( 'vendor' ) );
		},

		onDateChanged: function() {
			this.$( '.date' ).text( this.model.get( 'date' ) );
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
					display: 'block',
				} );
			} else {
				this.$el.css( {
					display: 'none',
				} );
			}
		},

		onStateChanged: function() {
			var updating = this.model.get( 'updating' );
			if( updating ) {
				this.$el.removeClass( 'success error' ).addClass( 'info' );
			} else {
				this.$el.removeClass( 'info' ).addClass( 'success' );
				var tmp = this.$el;
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

	var orderListView = new OrderListView( {
		el: '#orders',
		model: GalTrace.orderList,
	} );
} )();
