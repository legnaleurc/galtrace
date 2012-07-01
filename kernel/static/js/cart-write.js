/**
 * Create a new row.
 *
 * @param {Object} args JSON-parsed data.
 * @param {Function} callback callback function on success.
 * @returns {jqXHR} AJAX object.
 */
GalTrace.createRow = function( args ) {
	// send request, server will handle INSERT/UPDATE by itself
	var request = jQuery.post( GalTrace.urls.SAVE, args, null, 'json' );

	// find if exists (by title); can not use binary search here
	var row = null;
	var tmp = -1;
	jQuery.each( GalTrace.view.items, function( key, value ) {
		if( this.title === args.title ) {
			tmp = key;
			row = value;
			return false;
		}
	} );
	// only update data and move order if success
	if( row !== null ) {
		return request.success( function() {
			// update data and HTML
			row.update( args, tmp );
		} );
	}

	return request.success( function() {
		var row = new GalTrace.DynamicRow( args );
		var tmp = GalTrace.view.find( row );
		GalTrace.view.insert( tmp.index, row );

		// update hidden state
		var phasePass = GalTrace.matchPhase( row );
		if( phasePass ) {
			jQuery.merge( GalTrace.phaseSet, [ row.getElement() ] );
		}
		var searchPass = GalTrace.matchSearch( row );
		if( searchPass ) {
			jQuery.merge( GalTrace.searchSet, [ row.getElement() ] );
		}
		if( phasePass && searchPass ) {
			GalTrace.emit( 'GalTrace.currentOrdersChanged', 1 );
		} else {
			row.getElement().hide();
		}

		// update total count
		GalTrace.emit( 'GalTrace.totalOrdersChanged', 1 );
	} );
};

GalTrace.deleteRows = function() {
	var selected = GalTrace.view.view.children().filter( function() {
		return $( this ).data( 'checked' );
	} );
	var request = jQuery.post( GalTrace.urls.DELETE, {
		orders: jQuery.map( selected, function( value, key ) {
			return $( value ).data( 'title' );
		} ),
	}, null, 'json' ).success( function() {
		GalTrace.phaseSet = GalTrace.phaseSet.filter( function() {
			return !$( this ).data( 'checked' );
		} );
		GalTrace.searchSet = GalTrace.searchSet.filter( function() {
			return !$( this ).data( 'checked' );
		} );
		GalTrace.view.items = jQuery.grep( GalTrace.view.items, function( value, key ) {
			return !value.isChecked();
		} );
		var tmp = selected.filter( ':visible' );
		GalTrace.emit( 'GalTrace.currentOrdersChanged', -tmp.length );
		GalTrace.emit( 'GalTrace.totalOrdersChanged', -selected.length );
		selected.remove();
	} );
	return request;
};

GalTrace.movePhase = function( phase ) {
	var selected = jQuery.grep( GalTrace.view.items, function( value, key ) {
		return value.isChecked();
	} );
	var request = jQuery.post( GalTrace.urls.MOVE, {
		phase: phase,
		orders: jQuery.map( selected, function( value, key ) {
			return value.getTitle();
		} ),
	}, null, 'json' ).success( function() {
		jQuery.each( selected, function() {
			this.setPhase( phase );
			this.setChecked( false );
		} );
	} );
	return request;
};

/**
 * Take row from table.
 *
 * The DOM object is temporary removed, but still exist.
 *
 * @param {int} index The index to be remove.
 * @returns {GalTrace.Row} The taken row.
 */
GalTrace.Table.prototype.take = function( index ) {
	var taken = this.items.splice( index, 1 )[0];
	taken.getElement().detach();
	return taken;
};

GalTrace.Table.prototype.__post_new__ = function() {
	this.view.on( 'GalTrace.phaseOfRowChanged', function( event, row ) {
		if( GalTrace.selectedPhases[row.phase] ) {
			jQuery.merge( GalTrace.phaseSet, [ row.getElement() ] );
			row.getElement().show();
			GalTrace.emit( 'GalTrace.currentOrdersChanged', 1 );
		} else {
			var tmp = -1;
			jQuery.each( GalTrace.phaseSet, function( key, value ) {
				if( row.getElement().is( value ) ) {
					tmp = key;
					return false;
				}
			} );
			Array.prototype.splice.call( GalTrace.phaseSet, tmp, 1 );
			row.getElement().hide();
			GalTrace.emit( 'GalTrace.currentOrdersChanged', -1 );
		}
	} );

	this.view.on( 'GalTrace.rowOrderChanged', function( event, row, origIndex ) {
		GalTrace.view.take( origIndex );
		var tmp = GalTrace.view.find( row );
		GalTrace.view.insert( tmp.index, row );
	} );
};

/**
 * Set selection state.
 *
 * @param {boolean} checked selection state.
 * @returns {GalTrace.Row} self.
 */
GalTrace.Row.prototype.setChecked = function( checked ) {
	this.checkbox.attr( 'checked', checked );
	this.element.data( 'checked', checked );
	return this;
};

/**
 * Set complete phase.
 *
 * @param {int} phase Complete phase.
 * @returns {GalTrace.Row} self.
 */
GalTrace.Row.prototype.setPhase = function( phase ) {
	if( this.phase !== phase ) {
		this.phase = phase;
		this.element.data( 'phase', this.phase );
		GalTrace.emit( 'GalTrace.phaseOfRowChanged', [ this ] );
	}
	return this;
};

/**
 * Save row's change.
 *
 * @returns {jqXHR} A AJAX object.
 */
GalTrace.Row.prototype.save = function() {
	return jQuery.post( GalTrace.urls.SAVE, {
		title: this.title,
		vendor: this.vendor,
		date: this.date,
		uri: this.uri,
		phase: this.phase,
		volume: this.volume
	}, null, 'json' );
};

GalTrace.Row.prototype.update = function( data, origIndex ) {
	var orderChanged = false;

	if( this.title !== data.title ) {
		this.title = data.title;
		this.titleCell.text( this.title );
		this.element.data( 'title', this.title );
		orderChanged = true;
	}

	if( this.vendor !== data.vendor ) {
		this.vendor = data.vendor;
		this.vendorText.text( this.vendor );
		this.element.data( 'vendor', this.vendor );
	}

	if( this.date !== data.date ) {
		this.date = data.date;
		this.dateText.text( this.date );
		orderChanged = true;
	}

	if( this.uri !== data.uri ) {
		this.uri = data.uri;
		this.link.attr( 'href', this.uri );
	}

	if( this.phase !== data.phase ) {
		this.phase = data.phase;
		this.element.data( 'phase', this.phase );
		GalTrace.emit( 'GalTrace.phaseOfRowChanged', [ this ] );
	}

	this.volume = data.volume;

	if( orderChanged ) {
		GalTrace.emit( 'GalTrace.rowOrderChanged', [ this, origIndex ] );
	}
};

( function() {

	/**
	 * Show the inline edit widget.
	 *
	 * @param {jQuery} parent Parent HTML element.
	 * @param {jQuery} label The displaying label.
	 * @param {jQuery} input The editing widget.
	 */
	function openEdit( parent, label, input ) {
		input.width( parent.width() ).val( label.hide().text() ).show().select();
	}

	/**
	 * Hide the inline edit widget.
	 *
	 * @param {jQuery} label The displaying label.
	 * @param {jQuery} input The editing widget.
	 */
	function closeEdit( label, input ) {
		label.show();
		input.hide();
	}

	/**
	 * Commit content.
	 *
	 * @param {jQuery} label The displaying label.
	 * @param {jQuery} input The editing widget.
	 * @param {String} key Editing row's title.
	 * @param {String} field The field to be commit as change.
	 * @returns {jqXHR} The AJAX object.
	 */
	function saveEdit( label, input, key, field ) {
		if( label.text() == input.val() ) {
			return;
		}
		label.text( input.val() );
		var args = {
			title: key
		};
		args[field] = input.val();
		// TODO add hook
		return jQuery.post( GalTrace.urls.SAVE, args, null, 'json' );
	}

	/**
	 * Post-initialization.
	 *
	 * @protected
	 */
	GalTrace.DynamicRow.prototype.__post_new__ = function() {
			// checkbox cell
			this.selector = $( '<td></td>' );
			this.checkbox = $( '<input type="checkbox" />' ).change( GalTrace.bind( function( row ) {
				row.element.data( 'checked', row.checkbox.is( ':checked' ) );
			}, this ) );
			this.element.data( 'checked', false );
			this.selector.append( this.checkbox );
			this.element.prepend( this.selector );

			// vendor cell
			this.vendorEdit = $( '<input type="text" style="display: none;" />' ).blur( GalTrace.bind( function( row ) {
				saveEdit( row.vendorText, row.vendorEdit, row.title, 'vendor' );
				row.vendor = row.vendorText.text();
				closeEdit( row.vendorText, row.vendorEdit );
			}, this ) );
			this.vendorCell.dblclick( GalTrace.bind( openEdit, this.vendorCell, this.vendorText, this.vendorEdit ) );
			this.vendorCell.append( this.vendorEdit );

			// date cell
			this.dateEdit = $( '<input type="text" style="display: none;" />' ).blur( GalTrace.bind( function( row ) {
				if( /^\d\d\d\d\/\d\d\/\d\d$/.test( row.dateEdit.val() ) ) {
					saveEdit( row.dateText, row.dateEdit, row.title, 'date' );
					var result = GalTrace.view.find( row );
					GalTrace.view.take( result.index );
					row.date = row.dateText.text();
					result = GalTrace.view.find( row );
					GalTrace.view.insert( result.index, row );
				}
				closeEdit( row.dateText, row.dateEdit );
			}, this ) );
			this.dateCell.dblclick( GalTrace.bind( openEdit, this.dateCell, this.dateText, this.dateEdit ) );
			this.dateCell.append( this.dateEdit );
	};

} )();
