/**
 * @namespace All functionality of GalTrace.
 */
var GalTrace = {

	/**
	 * Bind function but leave this untouched.
	 *
	 * Unlike Function.bind in JavaScript 1.8, this version only binds
	 * arguments, the instance will not change.
	 *
	 * @param {Function} fn The binding function.
	 * @param [args ...] The binding arguments.
	 * @returns The binded function.
	 */
	bind: function( fn ) {
		var args = Array.prototype.slice.call( arguments, 1 );
		return function() {
			fn.apply( this, args.concat( Array.prototype.slice.call( arguments ) ) );
		};
	},

	/**
	 * Show error message.
	 *
	 * @param {String} title Error message title.
	 * @param {String} msg The error message.
	 */
	cerr: function( title, msg ) {
		$( '#error-title' ).text( title );
		$( '#error-message' ).text( msg );
		$( '#stderr' ).fadeIn( 'slow' );
	},

	emit: function( eventType, extraParameters ) {
		return GalTrace.view.view.trigger( eventType, extraParameters );
	},

	initialize: function( selector ) {
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
					GalTrace.phaseSet = GalTrace.view.view.children().filter( ':visible' );
					GalTrace.searchSet = GalTrace.view.view.children();
					GalTrace.emit( 'GalTrace.totalOrdersChanged', GalTrace.searchSet.length );
					GalTrace.emit( 'GalTrace.currentOrdersChanged', GalTrace.phaseSet.length );
					return;
				}
				data = data.data;

				load( offset + data.length );

				jQuery.each( data, function( key, value ) {
					var row = new GalTrace.DynamicRow( this );
					if( !GalTrace.matchPhase( row ) ) {
						row.getElement().hide();
					}
					GalTrace.view.append( row );
				} );
			} ).error( function( jqXHR, textStatus, message ) {
				GalTrace.cerr( 'Unknown Error', message );
			} );
		}

		GalTrace.view = new GalTrace.Table( selector );
		GalTrace.phaseSet = null;
		GalTrace.searchSet = null;
		GalTrace.selectedPhases = {
			0: true,
			1: false,
			2: false,
			3: false,
			4: false,
		};
		load( 0 );
	},

	/**
	 * Matches given condition.
	 *
	 * @param {String} pattern Matches title or vendor.
	 * @param {Array} phases Selected phases.
	 * @return {boolean} true if matched.
	 */
	matchPhase: function( row ) {
		return GalTrace.selectedPhases[row.phase];
	},

	/**
	 * Matches given condition.
	 *
	 * @param {String} pattern Matches title or vendor.
	 * @param {Array} phases Selected phases.
	 * @return {boolean} true if matched.
	 */
	matchSearch: function( row ) {
		var pattern = $( '#search' ).val().toLowerCase();
		return ( row.title.toLowerCase().indexOf( pattern ) >= 0 || row.vendor.toLowerCase().indexOf( pattern ) >= 0 );
	},

	/**
	 * Do nothing.
	 *
	 * @class Base class of table row.
	 */
	Row: function() {
		// NOTE base class
	},

	/**
	 * Creates table.
	 *
	 * @class The table.
	 * @param selector The selector on DOM.
	 */
	Table: function( selector ) {
		this.items = [];
		this.view = $( selector );
		this.view.on( 'GalTrace.currentOrdersChanged', function( event, diff ) {
			var tmp = $( '#current-orders' );
			tmp.text( parseInt( tmp.text(), 10 ) + diff );
		} );
		this.view.on( 'GalTrace.totalOrdersChanged', function( event, diff ) {
			var tmp = $( '#total-orders' );
			tmp.text( parseInt( tmp.text(), 10 ) + diff );
		} );
		this.view.on( 'GalTrace.phaseChanged', function( event, phase, selected ) {
			if( GalTrace.phaseSet === null || GalTrace.searchSet === null ) {
				return;
			}
			function eq() {
				return $( this ).data( 'phase' ) === phase;
			}
			GalTrace.selectedPhases[phase] = selected;
			if( selected ) {
				// some orders should be inserted, p += dp
				jQuery.merge( GalTrace.phaseSet, $( this ).children().filter( eq ) );
			} else {
				GalTrace.phaseSet = GalTrace.phaseSet.filter( function() {
					return !eq.bind( this )();
				} );
			}
			// ( s && dp ).setVisible( selected )
			var tmp = GalTrace.searchSet.filter( eq );
			if( selected ) {
				tmp.show();
				$( this ).trigger( 'GalTrace.currentOrdersChanged', tmp.length );
			} else {
				tmp.hide();
				$( this ).trigger( 'GalTrace.currentOrdersChanged', -tmp.length );
			}
		} );
		this.view.on( 'GalTrace.searchChanged', function( event, searchText, brandNew, increase ) {
			function eq() {
				var self = $( this );
				if( self.data( 'title' ).toLowerCase().indexOf( searchText.toLowerCase() ) >= 0 || self.data( 'vendor' ).toLowerCase().indexOf( searchText.toLowerCase() ) >= 0 ) {
					return true;
				}
				return false;
			}
			// if brand new search string, re-search whole orders
			// else if text length is increasing, strip from current visible set
			// else add new matched result to visible set
			if( brandNew ) {
				GalTrace.searchSet = $( this ).children().filter( eq );
				var a = GalTrace.phaseSet.filter( ':hidden' ).filter( eq );
				var b = GalTrace.phaseSet.filter( ':visible' ).filter( function() {
					return !eq.bind( this )();
				} );
				a.show();
				b.hide();
				$( this ).trigger( 'GalTrace.currentOrdersChanged', a.length - b.length );
			} else if( increase ) {
				GalTrace.searchSet = GalTrace.searchSet.filter( eq );
				var tmp = GalTrace.phaseSet.filter( ':visible' ).filter( function() {
					return !eq.bind( this )();
				} );
				tmp.hide();
				$( this ).trigger( 'GalTrace.currentOrdersChanged', -tmp.length );
			} else {
				GalTrace.searchSet = $( this ).children().filter( eq );
				var tmp = GalTrace.phaseSet.filter( ':hidden' ).filter( eq );
				tmp.show();
				$( this ).trigger( 'GalTrace.currentOrdersChanged', tmp.length );
			}
		} );

		this.__post_new__();
	},

	/**
	 * Create dynamic row from JSON data.
	 *
	 * @class Row from JSON to DOM.
	 * @param data The JSON data.
	 */
	DynamicRow: function( data ) {
		// call super
		GalTrace.Row.apply( this, arguments );

		// data
		this.title = data.title;
		this.vendor = data.vendor;
		this.date = data.date;
		this.uri = data.uri;
		this.phase = data.phase;
		this.volume = data.volume;

		// container element
		this.element = $( '<tr />' );

		// title cell
		this.titleCell = $( '<td class="title"></td>' ).text( this.title ).click( function( event ) {
			if( !event.ctrlKey && !event.metaKey || event.which != 1 ) {
				return;
			}
			GalTrace.googleSearch( $( this ).text() );
		} );

		// link cell
		this.linkCell = $( '<td></td>' );
		this.link = $( '<a rel="external"><i class="icon-link"></i></a>' ).click( function( event ) {
			event.preventDefault();
			window.open( $( this ).attr( 'href' ), '_blank' );
		} ).attr( 'href', this.uri );
		this.linkCell.append( this.link );

		// vendor cell
		this.vendorCell = $( '<td class="vendor" />' );
		this.vendorText = $( '<span />' ).text( this.vendor );
		this.vendorCell.append( this.vendorText );

		// date cell
		this.dateCell = $( '<td class="date" />' );
		this.dateText = $( '<span />' ).text( this.date );
		this.dateCell.append( this.dateText );

		this.element.append( this.titleCell ).append( this.linkCell ).append( this.vendorCell ).append( this.dateCell ).append( this.phaseCell );
		this.element.data( 'title', this.title );
		this.element.data( 'vendor', this.vendor );
		this.element.data( 'phase', this.phase );

		this.__post_new__();
	},

};

/**
 * Append a row to the table.
 *
 * @param {GalTrace.Row} row The appending row.
 * @returns {GalTrace.Table} self.
 */
GalTrace.Table.prototype.append = function( row ) {
	this.items.push( row );
	this.view.append( row.getElement() );

	return this;
};

/**
 * Find row in table.
 *
 * @param {GalTrace.Row} row The row to be found.
 * @param {Function} [compare] Comparator.
 * @returns {Object}
 * o.found indicates whether the row exists.
 * o.index indicates the position of row, or desired insert position.
 */
GalTrace.Table.prototype.find = function( row, compare ) {
	if( compare === undefined ) {
		compare = function( l, r ) {
			if( l.getDate() == r.getDate() ) {
				if( l.getTitle() == r.getTitle() ) {
					return 0;
				}
				return ( l.getTitle() < r.getTitle() ) ? -1 : 1;
			}
			return ( l.getDate() < r.getDate() ) ? -1 : 1;
		};
	}
	function binarySearch( row, list, begin, end ) {
		var middle = Math.floor( ( begin + end ) / 2 );
		var that = list[middle];
		var tmp = compare( row, that );
		if( tmp < 0 ) {
			if( end - begin == 1 ) {
				return {
					found: false,
					index: middle
				};
			} else {
				return binarySearch( row, list, begin, middle );
			}
		} else if( tmp > 0 ) {
			if( end - begin == 1 ) {
				return {
					found: false,
					index: end
				};
			} else {
				return binarySearch( row, list, middle, end );
			}
		} else {
			return {
				found: true,
				index: middle
			};
		}
	}
	return ( this.items.length == 0 ) ? {
		found: false,
		index: 0
	} : binarySearch( row, this.items, 0, this.items.length );
};

/**
 * Insert row to index.
 *
 * @param index After insertion, row will appear here.
 * @param row The row to be insert.
 * @return {GalTrace.Table} self.
 */
GalTrace.Table.prototype.insert = function( index, row ) {
	if( this.items.length == 0 ) {
		this.append( row );
	} else if( index >= this.items.length ) {
		this.items[ this.items.length - 1 ].getElement().after( row.getElement() );
		this.items.push( row );
	} else if( index > 0 ) {
		this.items[index].getElement().before( row.getElement() );
		this.items.splice( index, 0, row );
	} else {
		this.items[0].getElement().before( row.getElement() );
		this.items.splice( 0, 0, row );
	}
	return this;
};

GalTrace.Table.prototype.__post_new__ = function() {
};

/**
 * Get DOM jQuery object.
 *
 * @returns {jQuery} DOM object.
 */
GalTrace.Row.prototype.getElement = function() {
	return this.element;
};

/**
 * Selection state.
 *
 * @return {boolean} true if selected.
 */
GalTrace.Row.prototype.isChecked = function() {
	return this.checkbox.is( ":checked" );
};

/**
 * Get title.
 *
 * @returns {String} Title.
 */
GalTrace.Row.prototype.getTitle = function() {
	return this.title;
};

/**
 * Get release date.
 *
 * @returns {String} Release date.
 */
GalTrace.Row.prototype.getDate = function() {
	return this.date;
};

/**
 * Get complete phase.
 *
 * @returns {int} Complete phase.
 */
GalTrace.Row.prototype.getPhase = function() {
	return this.phase;
};

/**
 * Post-initialization.
 *
 * Please override this function.
 *
 * @protected
 */
GalTrace.Row.prototype.__post_new__ = function() {
	// NOTE this function provides a post-initialization
};

GalTrace.DynamicRow.prototype = new GalTrace.Row();
