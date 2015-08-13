(function(w) {
	// H5 plus事件处理
	var ws = null,
		as = 'slide-in-right',
		at = 200;
	
	if (w.plus) {
		plusReady();
	} else {
		document.addEventListener('plusready', plusReady, false);
	}

	// 处理返回事件
	w.back = function(hide) {
		if (w.plus) {
			ws || (ws = plus.webview.currentWebview());
			if (hide || ws.preate) {
				ws.hide('auto', at);
			} else {
				ws.close('auto', at);
			}
		} else if (history.length > 1) {
			history.back();
		} else {
			w.close();
		}
	};

	// 处理点击事件
	var openw = null,
		waiting = null;
	/**
	 * 打开新窗口
	 * @param {URIString} id : 要打开页面url
	 * @param {boolean} wa : 是否显示等待框
	 * @param {boolean} ns : 是否不自动显示
	 * @param {map} extras : 传递给新页面的额外参数
	 */
	w.changePage = function(id, wa, ns, extras) {
		if (openw) { //避免多次打开同一个页面
			openw.show('slide-in-right', 200);
			return null;
		}
		
		if (w.plus) {
			wa && (waiting = plus.nativeUI.showWaiting());
			var pre = ''; //'http://192.168.1.178:8080/h5/';
			openw = plus.webview.create(pre + id, id, {
				scrollIndicator: 'none',
				scalable: false,
				//bounce: 'vertical',
			}, extras);
			ns || openw.addEventListener('loaded', function() { //页面加载完成后才显示
				//		setTimeout(function(){//延后显示可避免低端机上动画时白屏
				openw.show(as, at);
				closeWaiting();
				//		},200);
			}, false);
			openw.addEventListener('close', function() { //页面关闭后可再次打开
				openw = null;
			}, false);

			return openw;
		} else {
			w.open(id);
		}
		return null;
	};
	
	w.pullfreshPage = function(header, content, title, extras) {
		var headerWebview = plus.webview.getWebviewById(header);
		if (!headerWebview) {
			headerWebview = mui.preload({
				url:header,
				id:header,
				styles:{
				},
				extras: {
					mType: "sub",
				},
			});
			
			headerWebview.addEventListener('loaded', function() {
				mui.fire(headerWebview,'updateHeader',{title:title});
			});			
		} else {
			mui.fire(headerWebview,'updateHeader',{title:title});
		}
		
		var contentWebview = plus.webview.getWebviewById(content);
		if (!contentWebview) {
			contentWebview = mui.preload({
				url:content,
				id:content,
				styles:{
					top: '45px',
					bottom: '0px',
				},
				extras:extras,
			});
			
			contentWebview.addEventListener('loaded', function() {
				mui.fire(contentWebview,'updateContent',extras);
				setTimeout(function() {
					contentWebview.show();
				}, 50);				
			});
			headerWebview.append(contentWebview);
		} else {
			mui.fire(contentWebview,'updateContent',extras);
		}

		contentWebview.show();
		headerWebview.show('slide-in-right', 150);		
	};

	/**
	 * 关闭等待框
	 */
	w.closeWaiting = function() {
		waiting && waiting.close();
		waiting = null;
	};
	
    function plusReady() {
		ws = plus.webview.currentWebview();
    }	
})(window);

(function($) {
	//全局配置(通常所有页面引用该配置，特殊页面使用mui.init({})来覆盖全局配置)
	$.initGlobal({
		swipeBack: true
	});

	var first = null;
	var back = $.back;
	$.back = function() {
		var current = plus.webview.currentWebview();
		if (current.mType == 'main') { //模板主页面
			//首次按键，提示‘再按一次退出应用’
			if (!first) {
				first = new Date().getTime();
				mui.toast('再按一次退出应用');
				setTimeout(function() {
					first = null;
				}, 1000);
			} else {
				if (new Date().getTime() - first < 1000) {
					plus.runtime.quit();
				}
			}
		} else if (current.mType == 'sub') {
			if ($.targets._popover) {
				$($.targets._popover).popover('hide');
			} else {
				current.parent().evalJS('mui&&mui.back();');
			}
		} else {
			back();
		}
	};    
})(mui);


var getState = function() {
	var stateText = localStorage.getItem('$state') || "{}";
	return JSON.parse(stateText);
};

var setState = function(state) {
	state = state || {};
	localStorage.setItem('$state', JSON.stringify(state));
};

var setSettings = function(settings) {
	settings = settings || {};
	localStorage.setItem('$settings', JSON.stringify(settings));
}
	
var getSettings = function() {
	var settingsText = localStorage.getItem('$settings') || "{}";
	return JSON.parse(settingsText);
}


