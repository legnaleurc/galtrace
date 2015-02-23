var GalTrace = GalTrace || {};
( function() {
	'use strict';

	var Order = Backbone.Model.extend( {
		defaults: {
			selected: false,
			updating: false,
		},
	} );

	var OrderList = Backbone.Collection.extend( {
		model: Order,

		comparator: function( l, r ) {
			if( l.get( 'date' ) === r.get( 'date' ) ) {
				if( l.get( 'title' ) === r.get( 'title' ) ) {
					return 0;
				}
				return ( l.get( 'title' ) < r.get( 'title' ) ) ? -1 : 1;
			}
			return ( l.get( 'date' ) < r.get( 'date' ) ) ? -1 : 1;
		},
	} );

	var OrderFilter = Backbone.Model.extend( {
		match: function( order ) {
			var phases = this.get( 'phases' );
			var qss = this.get( 'queryString' ).toLowerCase().trim().split( /\s+/ );
			var phase = order.get( 'phase' );
			var title = order.get( 'title' ).toLowerCase();
			var vendor = order.get( 'vendor' ).toLowerCase();

			return phases[phase] && [ title, vendor ].some( function( s ) {
				return qss.every( function( qs ) {
					return s.indexOf( qss ) >= 0;
				} );
			} );
		},
	} );

	GalTrace.Order = Order;
	GalTrace.orderList = new OrderList();
	GalTrace.orderFilter = new OrderFilter( {
		phases: {
			0: false,
			1: false,
			2: false,
			3: false,
			4: false,
		},
		queryString: '',
	} );
} )();
