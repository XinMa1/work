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
			
			cellphonen: {
				minlength: 8
			},
			
			passwd: {
				required: true,
				minlength: 4
			},
			nickname: {
				required: true,
				minlength: 2
			},
			
			name: {
				minlength: 2
			},
			
			phoneno: {
				minlength: 6
			},
			
			address: {
				minlength: 2
			},
			
			company: {
				minlength: 2
			},
			
			postcode: {
				minlength: 6
			},
			
			faxno: {
				minlength: 6
			},
			
			weibo: {
				minlength: 2
			},
			
			weixin: {
				minlength: 2
			},
			
			desc: {
			    minlength: 2
			},
			
			seq: {
				required: true,
			},
			
			contact:{
			    minlength: 2
			},
			
			fixedphone: {
				minlength: 7
			},
			
		},
		messages: {
		    
		},
	});


})();
