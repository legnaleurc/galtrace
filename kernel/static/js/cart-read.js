/**
 * @namespace All functionality of GalTrace.
 */
var Cart = {

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
		return Cart.view.view.trigger( eventType, extraParameters );
	},

	initialize: function( selector ) {
		function load( offset ) {
			jQuery.post( Cart.urls.LOAD, {
				offset: offset,
				limit: 100,
			}, null, 'json' ).success( function( data, textStatus, jqXHR ) {
				if( !data.success ) {
					Cart.cerr( data.type, data.message );
					return;
				}
				if( data.data === null ) {
					// load finished
					Cart.phaseSet = Cart.view.view.children().filter( ':visible' );
					Cart.searchSet = Cart.view.view.children();
					return;
				}
				data = data.data;

				load( offset + data.length );

				$( data ).each( function() {
					Cart.view.append( new Cart.DynamicRow( this ) );
				} );
			} ).error( function( jqXHR, textStatus, message ) {
				Cart.cerr( 'Unknown Error', message );
			} );
		}

		Cart.view = new Cart.Table( selector );
		Cart.phaseSet = null;
		Cart.searchSet = null;
		load( 0 );
	},

	/**
	 * Matches given condition.
	 *
	 * @param {String} pattern Matches title or vendor.
	 * @param {Array} phases Selected phases.
	 * @return {boolean} true if matched.
	 */
	applyFilter: function( row ) {
		// NOTE should only call by row's constructor
		// FIXME ugly global operation
		var phases = jQuery.map( $( '.phase-filter.active' ), function( v ) {
			return $( v ).data( 'value' );
		} );
		var pattern = $( '#search' ).val().toLowerCase();

		var patternPass = false;
		if( row.title.toLowerCase().indexOf( pattern ) >= 0 || row.vendor.toLowerCase().indexOf( pattern ) >= 0 ) {
			patternPass = true;
		}
		if( patternPass ) {
			jQuery.merge( Cart.searchSet, [ row.getElement() ] );
		}

		var phasePass = phases.indexOf( row.phase ) >= 0;
		if( phasePass ) {
			jQuery.merge( Cart.phaseSet, [ row.getElement() ] );
		}

		return patternPass && phasePass;
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
		this.view.on( 'GalTrace.phaseChanged', function( event, phase, selected ) {
			if( Cart.phaseSet === null || Cart.searchSet === null ) {
				return;
			}
			function eq() {
				return $( this ).data( 'phase' ) === phase;
			}
			if( selected ) {
				// some orders should be inserted, p += dp
				jQuery.merge( Cart.phaseSet, $( this ).children().filter( eq ) );
			} else {
				Cart.phaseSet = Cart.phaseSet.filter( function() {
					return !eq.bind( this )();
				} );
			}
			// ( s && dp ).setVisible( selected )
			var tmp = Cart.searchSet.filter( eq );
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
				Cart.searchSet = $( this ).children().filter( eq );
				var a = Cart.phaseSet.filter( ':hidden' ).filter( eq );
				var b = Cart.phaseSet.filter( ':visible' ).filter( function() {
					return !eq.bind( this )();
				} );
				a.show();
				b.hide();
				$( this ).trigger( 'GalTrace.currentOrdersChanged', a.length - b.length );
			} else if( increase ) {
				Cart.searchSet = Cart.searchSet.filter( eq );
				var tmp = Cart.phaseSet.filter( ':visible' ).filter( function() {
					return !eq.bind( this )();
				} );
				tmp.hide();
				$( this ).trigger( 'GalTrace.currentOrdersChanged', -tmp.length );
			} else {
				Cart.searchSet = $( this ).children().filter( eq );
				var tmp = Cart.phaseSet.filter( ':hidden' ).filter( eq );
				tmp.show();
				$( this ).trigger( 'GalTrace.currentOrdersChanged', tmp.length );
			}
		} );
	},

	/**
	 * Create dynamic row from JSON data.
	 *
	 * @class Row from JSON to DOM.
	 * @param data The JSON data.
	 */
	DynamicRow: function( data ) {
		// call super
		Cart.Row.apply( this, arguments );

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
			Cart.googleSearch( $( this ).text() );
		} );

		// link cell
		this.linkCell = $( '<td></td>' );
		this.link = $( '<a rel="external">Link</a>' ).click( function( event ) {
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

		// phase cell
		this.phaseCell = $( '<td class="phase"></d>' ).hide().text( this.phase );

		this.element.append( this.titleCell ).append( this.linkCell ).append( this.vendorCell ).append( this.dateCell ).append( this.phaseCell );
		this.element.data( 'title', this.title );
		this.element.data( 'vendor', this.vendor );
		this.element.data( 'phase', this.phase );

		// update hidden state
		var matched = Cart.applyFilter( this );
		if( matched ) {
			// FIXME assuming creation is insertion
			Cart.emit( 'GalTrace.currentOrdersChanged', 1 );
		} else {
			this.element.hide();
		}

		this.__post_new__();
	},

};

/**
 * Append a row to the table.
 *
 * @param {Cart.Row} row The appending row.
 * @returns {Cart.Table} self.
 */
Cart.Table.prototype.append = function( row ) {
	this.items.push( row );
	this.view.append( row.getElement() );

	var totalOrders = $( '#total-orders' );
	totalOrders.text( parseInt( totalOrders.text(), 10 ) + 1 );

	return this;
};

/**
 * Get index-th row.
 *
 * @param {int} index The row index.
 * @returns {Cart.Row} row.
 */
Cart.Table.prototype.at = function( index ) {
	return this.items[index];
};

/**
 * Get row's count.
 *
 * @returns {int} Total rows.
 */
Cart.Table.prototype.size = function() {
	return this.items.length;
};

/**
 * Find row in table.
 *
 * @param {Cart.Row} row The row to be found.
 * @param {Function} [compare] Comparator.
 * @returns {Object}
 * o.found indicates whether the row exists.
 * o.index indicates the position of row, or desired insert position.
 */
Cart.Table.prototype.find = function( row, compare ) {
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
 * @return {Cart.Table} self.
 */
Cart.Table.prototype.insert = function( index, row ) {
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

/**
 * Get DOM jQuery object.
 *
 * @returns {jQuery} DOM object.
 */
Cart.Row.prototype.getElement = function() {
	return this.element;
};

/**
 * Selection state.
 *
 * @return {boolean} true if selected.
 */
Cart.Row.prototype.isChecked = function() {
	return this.checkbox.is( ":checked" );
};

/**
 * Get title.
 *
 * @returns {String} Title.
 */
Cart.Row.prototype.getTitle = function() {
	return this.title;
};

/**
 * Get release date.
 *
 * @returns {String} Release date.
 */
Cart.Row.prototype.getDate = function() {
	return this.date;
};

/**
 * Get complete phase.
 *
 * @returns {int} Complete phase.
 */
Cart.Row.prototype.getPhase = function() {
	return this.phase;
};

/**
 * Post-initialization.
 *
 * Please override this function.
 *
 * @protected
 */
Cart.Row.prototype.__post_new__ = function() {
	// NOTE this function provides a post-initialization
};

Cart.DynamicRow.prototype = new Cart.Row();
