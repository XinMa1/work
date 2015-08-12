jQuery(document).ready(function(){
    var mapObj, mar;  
    
    function mapInit(lng, lat) {
        console.log(lng);
        console.log(lat);
        if (lng && lat) {
            mapObj=new AMap.Map("admin_map",{
                view: new AMap.View2D({
                    center:new AMap.LngLat(lng, lat),
                    zoom:15,
                    rotation:0
                }),
                lang:"zh_cn"//设置语言类型，中文简体
            });

            addMarker(lng, lat);
            mapObj.setFitView();
        } else {
            mapObj=new AMap.Map("admin_map",{
                view: new AMap.View2D({
                    zoom:15,
                    rotation:0
                }),
                lang:"zh_cn"//设置语言类型，中文简体
            });
        }

        //为地图注册click事件获取鼠标点击出的经纬度坐标  
        AMap.event.addListener(mapObj,'click',function(e){ 
            var lng = e.lnglat.getLng();
            var lat = e.lnglat.getLat();
            cleanMarker();
            addMarker(lng, lat);
            document.getElementById('longitude').value = lng;
            document.getElementById('latitude').value = lat;
        });
    }

    function cleanMarker(){
        mar && mar.setMap(null);
    }

    function goGeocoding(address) {  
        var MGeocoder;
        AMap.service(["AMap.Geocoder"], function() {        
            MGeocoder = new AMap.Geocoder({ 
                radius: 1000,
                extensions: "all"
            });

            MGeocoder.getLocation(address, function(status, result){
                if(status === 'complete' && result.info === 'OK'){
                    geocoder_CallBack(result);
                }
            });
        });
    }    

    //地理编码返回结果展示     
    function geocoder_CallBack(data){  
        //地理编码结果数组  
        var geocode = data.geocodes[0];
        console.log(geocode.location.getLng());
        console.log(geocode.location.getLat());

        if(geocode){
            cleanMarker();
            endLoc = new AMap.LngLat(geocode.location.getLng(),geocode.location.getLat());
            var markerOption = {  
                map: mapObj,                   
                position: endLoc,
            };

            mar = new AMap.Marker(markerOption);    
            document.getElementById('longitude').value = geocode.location.lng;
            document.getElementById('latitude').value = geocode.location.lat;
            mapObj.setFitView();
        }
    }

    //实例化点标记  
    function addMarker(lng, lat){  
        mar=new AMap.Marker({                    
            icon:"http://webapi.amap.com/images/marker_sprite.png",  
            position:new AMap.LngLat(lng, lat)  
        });  
        mar.setMap(mapObj);  //在地图上添加点  
    }


    jQuery("#show_marker").click(function(){
        var addr = jQuery.trim(document.getElementById("address").value);
        if(addr.length){
            goGeocoding(addr);
        }
    });

    var lng = jQuery.trim(document.getElementById('longitude').value);
    var lat = jQuery.trim(document.getElementById('latitude').value);
    mapInit(lng, lat);
});
