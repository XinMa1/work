jQuery(document).ready(function(){
    jQuery("#reload_category").click(function(){
        jQuery.getJSON("/admin/ajax/category/list", {}, function(result){
            if(result.status == 0){
                var options = [];
                jQuery.each(result.data, function(index, category){
                    options.push("<option value='"+category.id+"'>"+category.name+"</option>");
                });
                jQuery("#category").html(options.join(''));
            }
        });
    });
});

