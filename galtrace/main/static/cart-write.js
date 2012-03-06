Cart.Table.prototype.newRow = function( args, callback ) {
	var row = new Cart.DynamicRow( args );
	var result = this.find( row );
	if( result.found ) {
		// FIXME the remove here well delete record in database,
		// instead of update it, please check this in someday
		this.take( result.index ).remove();
	}
	this.insert( result.index, row );

	// update hidden state
	var filter = Cart.getFilter();
	if( row.isMatch( filter.pattern, filter.phases ) ) {
		row.getElement().show();
	} else {
		row.getElement().hide();
	}

	row.save().success( callback );

	return this;
};

Cart.Table.prototype.take = function( index ) {
	var taken = this.items.splice( index, 1 )[0];
	taken.getElement().detach();
	return taken;
};

Cart.Row.prototype.setChecked = function( checked ) {
	this.checkbox.attr( 'checked', checked );
	return this;
};

Cart.Row.prototype.setPhase = function( phase ) {
	this.phase = phase;
	return this;
};

Cart.Row.prototype.remove = function() {
	this.element.remove();

	return jQuery.post( 'delete.cgi', {
		title: this.title
	}, function( data, textStatus ) {
		if( textStatus != 'success' ) {
			Cart.cerr( data );
		}
	}, 'json' );
};

Cart.Row.prototype.save = function() {
	return jQuery.post( 'save.cgi', {
		title: this.title,
		vendor: this.vendor,
		date: this.date,
		uri: this.uri,
		phase: this.phase,
		volume: this.volume
	}, function( data, textStatus ) {
		if( textStatus != 'success' ) {
			Cart.cerr( data );
			return;
		}
	}, 'json' );
};

Cart.__utilities__ = {

	openEdit: function( parent, label, input ) {
		input.width( parent.width() ).val( label.hide().text() ).show().select();
	},

	closeEdit: function( label, input ) {
		label.show();
		input.hide();
	},

	saveEdit: function( label, input, key, field ) {
		if( label.text() == input.val() ) {
			return;
		}
		label.text( input.val() );
		var args = {
			title: key
		};
		args[field] = input.val();
		jQuery.post( 'save.cgi', args, function( data, textStatus ) {
			if( textStatus != 'success' ) {
				Cart.cerr( data );
			}
		} );
	},

};

Cart.StaticRow.prototype.__post_new__ = function() {
		// checkbox cell
		this.checkbox = this.element.find( 'input.check' );

		// vendor cell
		this.vendorEdit = this.vendorCell.children().last().blur( Cart.bind( function( row ) {
			Cart.__utilities__.saveEdit( row.vendorText, row.vendorEdit, row.title, 'vendor' );
			row.vendor = row.vendorText.text();
			Cart.__utilities__.closeEdit( row.vendorText, row.vendorEdit );
		}, this ) );
		this.vendorCell.dblclick( Cart.bind( Cart.__utilities__.openEdit, this.vendorCell, this.vendorText, this.vendorEdit ) );

		// date cell
		this.dateEdit = this.dateCell.children().last().blur( Cart.bind( function( row ) {
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
};

Cart.DynamicRow =  function( data ) {
	// call super
	Cart.Row.apply( this, arguments );

	// data
	this.title = data.title;
	this.vendor = data.vendor;
	this.date = data.date;
	this.uri = data.uri;
	this.phase = data.phase.toString();
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

	this.__post_new__();
};

Cart.DynamicRow.prototype = new Cart.Row();

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
