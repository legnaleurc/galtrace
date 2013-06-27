var GalTrace = GalTrace || {};
( function() {
	'use strict';

	var ORDER_TEMPLATE = _.template( $( '#order-template' ).html() );

	var OrderView = Backbone.View.extend( {
		tagName: 'div',
		className: 'orders',

		initialize: function() {
			this.model.on( 'change:title', this.onTitleChanged, this );
			this.model.on( 'change:vendor', this.onVendorChanged, this );
			this.model.on( 'change:date', this.onDateChanged, this );
			this.model.on( 'change:uri', this.onUriChanged, this );
			this.model.on( 'change:phase', this.onFilterChanged, this );
			this.model.on( 'change:selected', this.onSelectionChanged, this );
			this.model.on( 'change:updating', this.onStateChanged, this );
			GalTrace.orderFilter.on( 'change:phases change:queryString', this.onFilterChanged, this );

			// bookkeeping
			this.$el.data( 'view', this );
		},

		render: function() {
			var title = this.model.get( 'title' );
			var vendor = this.model.get( 'vendor' );
			var date = this.model.get( 'date' );
			var uri = this.model.get( 'uri' );
			var thumb = this.model.get( 'thumb' );
			var phase = this.model.get( 'phase' );

			var template = ORDER_TEMPLATE( {
				title: title,
				vendor: vendor,
				date: date,
				uri: uri,
				thumb: thumb,
				phase: phase,
				cid: this.model.cid,
			} );
			this.$el.html( template );

			if( !GalTrace.orderFilter.match( this.model ) ) {
				this.$el.addClass( 'hidden' );
			}

			return this;
		},

		onTitleChanged: function() {
			var title = this.model.get( 'title' );
			this.$( 'span.title' ).attr( {
				title: title,
			} ).text( title );
		},

		onVendorChanged: function() {
			var vendor = this.model.get( 'vendor' );
			this.$( 'span.vendor' ).attr( {
				title: vendor,
			} ).text( vendor );
		},

		onDateChanged: function() {
			var date = this.model.get( 'date' );
			this.$( 'span.date' ).text( date );
		},

		onUriChanged: function() {
			this.$( '.uri' ).attr( {
				href: this.model.get( 'uri' ),
			} );
		},

		onFilterChanged: function() {
			if( GalTrace.orderFilter.match( this.model ) ) {
				this.$el.removeClass( 'hidden' );
			} else {
				this.$el.addClass( 'hidden' );
			}
		},

		onSelectionChanged: function() {
			if( this.model.get( 'selected' ) ) {
				this.$( '.check-btn' ).addClass( 'checked' );
			} else {
				this.$( '.check-btn' ).removeClass( 'checked' );
			}
		},

		onStateChanged: function() {
			var updating = this.model.get( 'updating' );
			if( updating ) {
				this.$el.removeClass( 'success error' ).addClass( 'updating' );
			} else {
				var tmp = window.innerHeight / 2;
				$( 'html, body' ).animate( {
					scrollTop: this.$el.offset().top - tmp,
				}, 1000 );
				this.$el.removeClass( 'updating' ).addClass( 'success' );
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
			this.model.on( 'sort', this.onSort, this );
		},

		onAdd: function( model_, collection, options ) {
			var view = new OrderView( {
				model: model_,
			} );
			var children = this.$el.children();
			var index = collection.indexOf( model_ );
			if( children.length === 0 || index > children.length ) {
				// first but empty
				// or overflowed
				this.$el.append( view.$el );
			} else if( index === children.length ) {
				// last
				children.last().after( view.$el );
			} else if( index > 0 ) {
				// middle
				$( children[index] ).before( view.$el );
			} else {
				// first
				children.first().before( view.$el );
			}
			view.render();
		},

		onRemove: function( model_, collection, options ) {
			$( this.$el.children()[options.index] ).remove();
		},

		onSort: function() {
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

	var CurrentCounterView = Backbone.View.extend( {
		initialize: function() {
			this.model.on( 'add', this.onAdd, this );
			this.model.on( 'remove', this.onRemove, this );
			GalTrace.orderFilter.on( 'change:phases change:queryString', this.onFilterChanged, this );

			this.render();
		},

		render: function() {
			var phases = GalTrace.orderFilter.get( 'phases' );
			var count = this.model.filter( function( model ) {
				return phases[model.get( 'phase' )];
			} ).length;;
			this.$el.text( count );
		},

		onAdd: function( model ) {
			model.on( 'change:phase', this.onModelPhaseChange, this );
			if( GalTrace.orderFilter.match( model ) ) {
				this.$el.text( parseInt( this.$el.text(), 10 ) + 1 );
			}
		},

		onRemove: function( model ) {
			if( GalTrace.orderFilter.match( model ) ) {
				this.$el.text( parseInt( this.$el.text(), 10 ) - 1 );
			}
		},

		onFilterChanged: function() {
			var count = this.model.filter( function( model ) {
				return GalTrace.orderFilter.match( model );
			} ).length;
			this.$el.text( count );
		},

		onModelPhaseChange: function( model_, value ) {
			if( GalTrace.orderFilter.get( 'phases' )[value] ) {
				this.$el.text( parseInt( this.$el.text(), 10 ) + 1 );
			} else {
				this.$el.text( parseInt( this.$el.text(), 10 ) - 1 );
			}
		},
	} );

	var TotalCounterView = Backbone.View.extend( {
		initialize: function() {
			this.model.on( 'add', this.onAdd, this );
			this.model.on( 'remove', this.onRemove, this );

			this.render();
		},

		render: function() {
			this.$el.text( this.model.length );
		},

		onAdd: function() {
			this.render();
		},

		onRemove: function( model ) {
			this.render();
		},
	} );

	var PhaseView = Backbone.View.extend( {
		initialize: function() {
			this.children = this.$el.children();
			// apply filter
			this.children.click( function( event ) {
				event.preventDefault();
				var self = $( this );
				self.toggleClass( 'active' );
				var tmp = GalTrace.orderFilter.get( 'phases' );
				tmp[self.data( 'value' )] = self.hasClass( 'active' );
				GalTrace.orderFilter.set( 'phases', tmp );
				// FIXME somehow I must trigger this manually
				GalTrace.orderFilter.trigger( 'change:phases' );
			} );
			// set initial filter
			this.children[0].click();
		},

		render: function() {
		},
	} );

	var QueryView = Backbone.View.extend( {
		initialize: function() {
			// query on-the-fly
			var previous = this.$el.text();
			this.$el.keyup( function( event ) {
				var current = $( this ).val();
				if( previous !== current ) {
					GalTrace.orderFilter.set( 'queryString', current );
					GalTrace.orderFilter.trigger( 'change:queryString' );
					previous = current;
				}
			} );
		},

		render: function() {
		},
	} );

	var orderListView = new OrderListView( {
		el: '#orders',
		model: GalTrace.orderList,
	} );
	var currentCounterView = new CurrentCounterView( {
		el: '#current-orders',
		model: GalTrace.orderList,
	} );
	var totalCounterView = new TotalCounterView( {
		el: '#total-orders',
		model: GalTrace.orderList,
	} );
	var phaseView = new PhaseView( {
		el: '#phases',
		model: GalTrace.orderFilter,
	} );
	var queryView = new QueryView( {
		el: '#query-string',
		model: GalTrace.orderFilter,
	} );
} )();
