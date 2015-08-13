(function(){
	var _j = jQuery.noConflict();
	_j("#formvalidate").validate({
		rules: {
		    email: {
				email: true
			},
			
			cellphone: {
			    required:true,
				minlength: 8
			},
			passwd: {
				required: true,
				minlength: 6
			},
			
			name: {
				minlength: 2
			},
			
			address: {
				minlength: 2
			},
			desc: {
			    minlength: 2
			},
		},
		messages: {
		    
		},
	});


})();
