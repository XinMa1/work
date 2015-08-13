jQuery(document).ready(function(){
        var _j = jQuery.noConflict();
        function reload_insert_thumbnail_list(album){
            var div = _j("#insert_thumbnail_list").children("div").addClass("hidden").filter("#insert_thumbnail_list_"+album);
            div.html("Loading...").removeClass("hidden");
            _j.getJSON("/admin/ajax/image/images", {album: album},
                       function(result){
                           if(result.status !== 0){
                               div.html(result.msg);
                           }else{
                               var content = [];
                               _j.each(result.data, function(index, img){
                                    if(index > 0 && index %3 === 0){
                                        content.push("<br/><br/>");
                                    }
                                    content.push('<input type="radio" value="'+img.src+'" data-img="'+img.id+'" name="insert_thumbnail_raido"><img src="'+img.url+'" alt="'+img.desc+'"/></input>');
                               });
                               div.html(content.join(''));
                           }
                       });
        }
        _j("#insert_img_album").change(function(){
            var sel_category = _j(this).val();
            reload_insert_thumbnail_list(sel_category);
        });
        _j("#toggle_select_thumbnail").click(function(){
            _j("#insert_thumbnail_list").toggle();
        });
        _j("#reload_insert_thumbnail").click(function(){
            reload_insert_thumbnail_list(_j("#insert_img_album").val());
        });
        _j("#insert_select_thumbnail").click(function(){
            var img_src = _j(":radio[name='insert_thumbnail_raido']:checked").val();
            var img_id = _j(":radio[name='insert_thumbnail_raido']:checked").data("img");
            if(window._tmp_edit_obj){
                window._tmp_edit_obj.execCommand("insertimage", 0, img_src);
                _j(window._tmp_edit_obj).find("img[src='"+img_src+"']").attr("width","100%");
                _j("#insert_thumbnail_list").hide();
                _j("#last_insert_image").val(img_id);
            }
        });
});
