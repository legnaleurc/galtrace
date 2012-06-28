/**
 * Create a new row.
 *
 * @param {Object} args JSON-parsed data.
 * @param {Function} callback callback function on success.
 * @returns {jqXHR} AJAX object.
 */
Cart.Table.prototype.newRow = function( args ) {
	var row = new Cart.DynamicRow( args );
	var result = this.find( row );
	if( result.found ) {
		// FIXME the remove here well delete record in database,
		// instead of update it, please check this in someday
		this.take( result.index ).remove();
	}
	this.insert( result.index, row );

	return row.save();
};

/**
 * Take row from table.
 *
 * The DOM object is temporary removed, but still exist.
 *
 * @param {int} index The index to be remove.
 * @returns {Cart.Row} The taken row.
 */
Cart.Table.prototype.take = function( index ) {
	var taken = this.items.splice( index, 1 )[0];
	taken.getElement().detach();
	return taken;
};

/**
 * Set selection state.
 *
 * @param {boolean} checked selection state.
 * @returns {Cart.Row} self.
 */
Cart.Row.prototype.setChecked = function( checked ) {
	this.checkbox.attr( 'checked', checked );
	return this;
};

/**
 * Set complete phase.
 *
 * @param {int} phase Complete phase.
 * @returns {Cart.Row} self.
 */
Cart.Row.prototype.setPhase = function( phase ) {
	this.phase = phase;
	return this;
};

/**
 * Totally remove row from DOM and database.
 *
 * @returns {jqXHR} A AJAX object.
 */
Cart.Row.prototype.remove = function() {
	this.element.remove();

	return jQuery.post( Cart.urls.DELETE, {
		title: this.title
	}, null, 'json' );
};

/**
 * Save row's change.
 *
 * @returns {jqXHR} A AJAX object.
 */
Cart.Row.prototype.save = function() {
	return jQuery.post( Cart.urls.SAVE, {
		title: this.title,
		vendor: this.vendor,
		date: this.date,
		uri: this.uri,
		phase: this.phase,
		volume: this.volume
	}, null, 'json' );
};

/**
 * @namespace Internal namespace.
 * @private
 */
Cart.__utilities__ = {

	/**
	 * Show the inline edit widget.
	 *
	 * @param {jQuery} parent Parent HTML element.
	 * @param {jQuery} label The displaying label.
	 * @param {jQuery} input The editing widget.
	 */
	openEdit: function( parent, label, input ) {
		input.width( parent.width() ).val( label.hide().text() ).show().select();
	},

	/**
	 * Hide the inline edit widget.
	 *
	 * @param {jQuery} label The displaying label.
	 * @param {jQuery} input The editing widget.
	 */
	closeEdit: function( label, input ) {
		label.show();
		input.hide();
	},

	/**
	 * Commit content.
	 *
	 * @param {jQuery} label The displaying label.
	 * @param {jQuery} input The editing widget.
	 * @param {String} key Editing row's title.
	 * @param {String} field The field to be commit as change.
	 * @returns {jqXHR} The AJAX object.
	 */
	saveEdit: function( label, input, key, field ) {
		if( label.text() == input.val() ) {
			return;
		}
		label.text( input.val() );
		var args = {
			title: key
		};
		args[field] = input.val();
		// TODO add hook
		return jQuery.post( Cart.urls.SAVE, args, null, 'json' );
	},

};

/**
 * Post-initialization.
 *
 * @protected
 */
Cart.DynamicRow.prototype.__post_new__ = function() {
		// checkbox cell
		this.selector = $( '<td></td>' );
		this.checkbox = $( '<input type="checkbox" class="check" />' );
		this.selector.append( this.checkbox );
		this.element.prepend( this.selector );

		// vendor cell
		this.vendorEdit = $( '<input type="text" style="display: none;" />' ).blur( Cart.bind( function( row ) {
			Cart.__utilities__.saveEdit( row.vendorText, row.vendorEdit, row.title, 'vendor' );
			row.vendor = row.vendorText.text();
			Cart.__utilities__.closeEdit( row.vendorText, row.vendorEdit );
		}, this ) );
		this.vendorCell.dblclick( Cart.bind( Cart.__utilities__.openEdit, this.vendorCell, this.vendorText, this.vendorEdit ) );
		this.vendorCell.append( this.vendorEdit );

		// date cell
		this.dateEdit = $( '<input type="text" style="display: none;" />' ).blur( Cart.bind( function( row ) {
			if( /^\d\d\d\d\/\d\d\/\d\d$/.test( row.dateEdit.val() ) ) {
				Cart.__utilities__.saveEdit( row.dateText, row.dateEdit, row.title, 'date' );
				var result = Cart.view.find( row );
				Cart.view.take( result.index );
				row.date = row.dateText.text();
				result = Cart.view.find( row );
				Cart.view.insert( result.index, row );
			}
			Cart.__utilities__.closeEdit( row.dateText, row.dateEdit );
		}, this ) );
		this.dateCell.dblclick( Cart.bind( Cart.__utilities__.openEdit, this.dateCell, this.dateText, this.dateEdit ) );
		this.dateCell.append( this.dateEdit );
};
