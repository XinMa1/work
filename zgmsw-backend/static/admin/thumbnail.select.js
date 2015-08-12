jQuery(document).ready(function(){
        var _j = jQuery.noConflict();
        function reload_thumbnail_list(album){
            var div = _j("#thumbnail_list").children("div").addClass("hidden").filter("#thumbnail_list_"+album);
            div.html("Loading...").removeClass("hidden");
            _j.getJSON("/admin/images/ajaximages", {album: album},
                       function(result){
                           if(result.status !== 0){
                               div.html(result.msg);
                           }else{
                               var content = [];
                               var current_img = _j("#thumbnail").val();
                               _j.each(result.data, function(index, img){
                                    if(index > 0 && index %3 === 0){
                                        content.push("<br/><br/>");
                                    }
                                    content.push('<input type="radio" value="'+img.id+'" name="thumbnail_raido"'+ (img.id == current_img ? " checked='checked' " : "") + '><img src="'+img.url+'" alt="'+img.descrition+'"/></input>');
                               });
                               div.html(content.join(''));
                           }
                       });
        }
        _j("#img_album").change(function(){
            var sel_category = _j(this).val();
            reload_thumbnail_list(sel_category);
        });
        _j("#select_thumbnail").click(function(){
            _j("#thumbnail_list").toggle();
        });

_j("#file").change(function(){
           var input = _j("#file");
           var formdata = false;
           if (window.FormData) {
              formdata = new FormData();
            }
            var i = 0, len = this.files.length, img, reader, file;
            for ( ; i < len; i++ ) {
                 file = this.files[i];
                 formdata.append("file", file);
            }
			     _j.ajax({
                type: "POST",
                url: '/admin/upload/image_default',
                data: formdata,
                success: function(){alert("upload sucess")},
                processData: false,
                dataType: false,
                contentType: false
            });
        });

        _j("#reload").click(function(){
            reload_thumbnail_list(_j("#img_album").val());
        });
        _j(document).on('click', ":radio[name='thumbnail_raido']", {},
                        function(){
                            _j("#current_thumbnail").attr("src","/admin/images/thumbnail?id="+_j(this).val());
                            _j("#thumbnail").val(_j(this).val());
                        });
});
