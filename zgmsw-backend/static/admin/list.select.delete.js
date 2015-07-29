jQuery(document).ready(function(){
    var _j = jQuery.noConflict();
 
    // add multiple select / deselect functionality 
    _j("#selectall").click(function () {
        _j('.case').prop('checked', this.checked);          
    });
    // if all checkbox are selected, check the selectall checkbox
    // and viceversa
    _j(".case").click(function(){
        if(_j(".case").length == _j(".case:checked").length) {
            _j("#selectall").prop("checked", true);
        } else {
            _j("#selectall").prop("checked", false);
        }
    });
    /* 批量删除 */
    _j("#deleteBatch").click(function() {
        // 判断是否至少选择一项
        var checkedNum = _j(".case:checked").length;
        if(checkedNum == 0) {
            alert("请选择至少一项！");
            return;
        }
        // 批量选择
        if(confirm("确定要删除所选项目？")) {
            var checkedList = new Array();
            _j(".case:checked").each(function() {
            checkedList.push(_j(this).val());
        });
        var url = _j("a[id='deleteBatch']").attr("name").toString();
        _j.ajax({
            type: "POST",
            url : "/admin/"+url+"/deleteBatch",
            data: {'delitems':checkedList.toString()},
            success: function(result) {
                _j(".case:checked").prop("checked", false);
                _j("#selectall").prop("checked", false);
                window.location.reload();
            }
        });
        }
    });
});