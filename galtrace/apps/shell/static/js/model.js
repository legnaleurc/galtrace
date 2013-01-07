var GalTrace = GalTrace || {};
( function() {
	'use strict';

	GalTrace.bind = function( fn ) {
		var args = Array.prototype.slice.call( arguments, 1 );
		return function() {
			fn.apply( this, args.concat( Array.prototype.slice.call( arguments ) ) );
		};
	};

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

	GalTrace.orderList = new OrderList();

	GalTrace.orderFilter = new Backbone.Model( {
		phases: {
			0: false,
			1: false,
			2: false,
			3: false,
			4: false,
		},
		search: '',
	} );

	GalTrace.initialize = function() {
		function load( offset ) {
			jQuery.post( GalTrace.urls.LOAD, {
				offset: offset,
				limit: 100,
			}, null, 'json' ).success( function( data, textStatus, jqXHR ) {
				if( !data.success ) {
					GalTrace.cerr( data.type, data.message );
					return;
				}
				if( data.data === null ) {
					// load finished
					return;
				}
				data = data.data;

				load( offset + data.length );

				GalTrace.orderList.add( data );
			} ).error( function( jqXHR, textStatus, message ) {
				GalTrace.cerr( 'Unknown Error', message );
			} );
		}

		load( 0 );
	};

	GalTrace.addOrder = function( args ) {
		// send request, server will handle INSERT/UPDATE by itself
		var request = jQuery.post( GalTrace.urls.SAVE, args, null, 'json' );

		// find if exists (by title); can not use binary search here
		var model = GalTrace.orderList.find( function( model_ ) {
			return model_.get( 'title' ) === args.title;
		} );
		// only update data and move order if success
		if( model !== undefined ) {
			model.set( 'updating', true );
			return request.success( function() {
				// update data and HTML
				model.set( {
					title: args.title,
					vendor: args.vendor,
					date: args.date,
					uri: args.uri,
					phase: args.phase,
					volume: args.volume,
					updating: false,
				} );
				GalTrace.orderList.sort();
			} );
		}

		return request.success( function() {
			var model = new Order( args );
			GalTrace.orderList.add( model );
		} );
	};

	GalTrace.movePhase = function( phase ) {
		var selected = GalTrace.orderList.filter( function( model ) {
			return model.get( 'selected' );
		} );
		var request = jQuery.post( GalTrace.urls.MOVE, {
			phase: phase,
			orders: _.map( selected, function( value ) {
				return value.get( 'title' );
			} ),
		}, null, 'json' ).success( function() {
			_.each( selected, function( element ) {
				element.set( {
					phase: phase,
					selected: false,
				} );
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
		}, null, 'json' ).success( function() {
			GalTrace.orderList.remove( selected );
		} );
		return request;
	};

	GalTrace.cerr = function( type, message ) {
		console.error( [ type, ': ', message ].join( '' ) );
	};
} )();
