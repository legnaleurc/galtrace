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
	 * @param {String} selector Where error message will show.
	 * @param {String} msg The error message.
	 */
	cerr: function( selector, msg ) {
		var tmp = $( '<div class="alert alert-error"><a class="close" href="#" data-dismiss="alert">&times;</a></div>' );
		tmp.appendTo( selector );
		tmp.append( $( '<span/>' ).text( msg ) );
	},

	/**
	 * Get phase filter from UI.
	 *
	 * @returns {Object} o.pattern contains name filter. o.phases is a array.
	 */
	getFilter: function() {
		var input = jQuery.map( $( '.phase-filter.active' ), function( v ) {
			return $( v ).data( 'value' );
		} );
		var phases_ = ( input.length === 0 ) ? null : {};
		if( phases_ ) {
			for( var i = 0; i < 5; ++i ) {
				phases_[i] = ( input.indexOf( i ) >= 0 );
			}
		}
		return {
			pattern: $( '#search' ).val(),
			phases: phases_,
		};
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
	 * Create rows from static page.
	 *
	 * @class Pre-exists row.
	 * @augments Cart.Row
	 * @param element The selector of row.
	 */
	StaticRow: function( element ) {
		// call super
		Cart.Row.apply( this, arguments );

		// container element
		this.element = $( element );

		// title cell
		this.titleCell = this.element.find( 'td.title' ).click( function( event ) {
			if( !event.ctrlKey && !event.metaKey || event.which != 1 ) {
				return;
			}
			Cart.googleSearch( $( this ).text() );
		} );
		this.title = this.titleCell.text();

		// link cell
		this.link = this.element.find( 'td > a' );
		this.linkCell = this.link.parent();
		this.uri = this.link.attr( 'href' );

		// vendor cell
		this.vendorCell = this.element.find( 'td.vendor' );
		this.vendorText = this.vendorCell.children().first();
		this.vendor = this.vendorText.text();

		// date cell
		this.dateCell = this.element.find( 'td.date' );
		this.dateText = this.dateCell.children().first();
		this.date = this.dateText.text();

		// phase
		this.phase = this.element.data( 'phase' );

		this.__post_new__();
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
		this.view.children().each( Cart.bind( function( table ) {
			var row = new Cart.StaticRow( this );
			table.items.push( row );
		}, this ) );
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
 * Update displaying rows according to UI selection.
 *
 * @returns {Cart.Table} self.
 */
Cart.Table.prototype.updateFilter = function() {
	var filter = Cart.getFilter();
	for( var i = 0; i < this.items.length; ++i ) {
		if( this.items[i].isMatch( filter.pattern, filter.phases ) ) {
			this.items[i].getElement().show();
		} else {
			this.items[i].getElement().hide();
		}
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
 * Matches given condition.
 *
 * @param {String} pattern Matches title or vendor.
 * @param {Array} phases Selected phases.
 * @return {boolean} true if matched.
 */
Cart.Row.prototype.isMatch = function( pattern, phases ) {
	var patternPass = false;
	var lPattern = pattern.toLowerCase();
	if( pattern.length == 0 || this.title.toLowerCase().indexOf( lPattern ) != -1 || this.vendor.toLowerCase().indexOf( lPattern ) != -1 ) {
		patternPass = true;
	}

	var phasePass = ( phases == null );
	if( !phasePass ) {
		phasePass = phases[this.phase];
	}

	return patternPass && phasePass;
}

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

Cart.StaticRow.prototype = new Cart.Row();
