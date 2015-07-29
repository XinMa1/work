# -*- coding: utf-8 -*-
#coding=utf-8

import config
from actions.admin.base import adminAction
from models.products import Products
from models.categories import Categories
from models.images import Images
from models.albums import Albums
from models.users import Users
from models.groups import Groups
from models.product_comments import ProductComments
from models.product_favorites import ProductFavorites
from models.product_rankings import ProductRankings
'''
Admin controller: producing product administration views.
'''
class refererAction(adminAction):
    def __init__(self, name = '产品管理'):
        adminAction.__init__(self, name)

    def GET(self, name):
        if name == 'list':
            return self.list()
        elif name == 'add':
            return self.add()
        elif name == 'delete':
            return self.delete()
        elif name == 'edit':
            return self.edit()
        elif name == 'map':
            return self.map()
        elif name == 'comments':
            return self.comments()
        elif name == 'commdelete':
            return self.commdelete()
        elif name == 'favorites':
            return self.favorite()
        elif name == 'favdelete':
            return self.favdelete()
        elif name == 'ranklist':
            return self.ranklist()
        elif name == 'rankdelete':
            return self.rankdelete()
        elif name == 'videos':
            return self.videos()
        else:
            return self.notFound()

    def POST(self, name):
        if name == 'save':
            return self.save()
        elif name == 'update':
            return self.update()
        elif name == 'search':
            return self.search()
        elif name == 'searchbycategory':
	    return self.searchbycategory()
        elif name == 'deleteBatch':
            return self.deleteBatch()
        elif name == 'commupdate':
            return self.commupdate()
        elif name == 'link':
            return self.link()

        return self.notFound()

    def list(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
        categoriesList = Categories.select()
        productsList = Products.select()

        current_user = Users.get(Users.name == self.isLogin())
        if not self.isAdmin():
            productsList = productsList.where(Products.owner == current_user)

        productsList = productsList.order_by(Products.id.desc()) 
        pageString = self.getPageStr('/admin/products/list', page, count, productsList.count())
        self.privData['PRODUCTS_LIST'] = productsList.paginate(page, page+count)
        self.privData['PAGE_STRING'] = pageString
        self.privData['CATEGORIES_LIST'] = categoriesList
        return self.display('productsList')

    def search(self):
        inputParams = self.getInput()
        keywords = inputParams['keywords'].strip().lower() if inputParams.has_key('keywords') else ''

        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
        categoriesList = Categories.select()
        productsList = Products.select().where(Products.name.contains(keywords))

        current_user = Users.get(Users.name == self.isLogin())
        if not self.isAdmin():
            productsList = productsList.where(Products.owner == current_user)

        productsList = productsList.order_by(Products.id.desc())
        pageString = self.getPageStr('/admin/products/list', page, count, productsList.count())
        self.privData['PRODUCTS_LIST'] = productsList.paginate(page, page+count)
        self.privData['PAGE_STRING'] = pageString
        self.privData['CATEGORIES_LIST'] = categoriesList
        return self.display('productsList')
 

    def searchbycategory(self):
        inputParams = self.getInput()
        categoryName = inputParams['categoryselect'].strip().lower() if inputParams.has_key('categoryselect') else ''
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE

        categoriesList = Categories.select()
        productsList = Products.select().where(Products.category == categoryName)
        current_user = Users.get(Users.name == self.isLogin())
        if not self.isAdmin():
            productsList = productsList.where(Products.owner == current_user)

        productsList = productsList.order_by(Products.id.desc()) 
        pageString = self.getPageStr('/admin/products/list', page, count, productsList.count())
        self.privData['PRODUCTS_LIST'] = productsList.paginate(page, page+count)
        self.privData['PAGE_STRING'] = pageString
        self.privData['CATEGORIES_LIST'] = categoriesList
        return self.display('productsList')

        
    def delete(self):
        inputParams = self.getInput()
        try:
            productID = inputParams['id']
            product = Products.get(Products.id == productID)
            product.delete_instance()
        except Exception, e:
            return self.success(msg='产品删除失败: %s' % e, url=self.makeUrl('/admin/products/list'))

        return self.success(msg='产品删除成功', url=self.makeUrl('/admin/products/list'))

    def edit(self):
        inputParams = self.getInput()
        productID = int(inputParams['id'])
        product = Products.get(Products.id == productID)
        userName = self.isLogin()

        categoriesList = Categories.select()
        self.privData['CATEGORIES_LIST'] = categoriesList

        user = Users.get(Users.name == userName)
        if user != product.owner and not self.isAdmin() or not user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/products/list'))

        groupsList = Groups().select().where(Groups.owner == user.id)
        self.privData['GROUPS_LIST'] = groupsList
        albumsList = Albums().select().where(Albums.owner == user.id)
        imagesList = Images().select().where(Images.owner == user.id)

                # 确认当前用户是否至少有一个包含图片的专辑
        if not albumsList.count():
            return self.error(msg = '请创建至少一个专辑!', url=self.makeUrl('/admin/products/list'))
        if not imagesList.count():
            return self.error(msg = '请创建至少一个图片!', url=self.makeUrl('/admin/products/list'))

        # 构建{album: images}, 同时排除不包括任何图片的专辑
        album_images_map = {}
        excluded_albums = []
        for album in albumsList:
            album_images = imagesList.where(Images.album == album.id)
            if album_images.count():
                album_images_map[album.id] = album_images
            else:
                excluded_albums.append(album.id)

        self.privData['ALBUMS_LIST'] = \
            [album for album in albumsList if album.id not in excluded_albums]
        self.privData['IMG_ALBUMS_LIST'] = album_images_map

        self.privData['CURRENT_OBJECT'] = product
        self.privData['CURRENT_ALBUM'] = product.thumbnail.album
        self.privData['CURRENT_IMG'] = product.thumbnail
        self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('productEdit')

    def update(self):
        inputParams= self.getInput()  
        productId = inputParams['id']
        try:
            price = float(inputParams['price'])
            discount = float(inputParams['discount'])
        except ValueError as ve:
            return self.error(msg = '产品修改失败: 价格或折扣格式有误，需要是数字', url=self.makeUrl('/admin/product/list'))

        try:
            product = Products.get(Products.id == productId)
            current_user = Users.get(Users.name == self.isLogin())
            if current_user.id != product.owner.id and not self.isAdmin() or not current_user.role.type < 100:
                return self.error(msg = '权限不足!', url=self.makeUrl('/admin/products/list'))

            q = Products.update(
                    price = price,
                    discount= discount,
                    description = self.htmlunquote(inputParams['desc']),
                    thumbnail = int(inputParams['thumbnail']),
                    group=int(inputParams['group']),
                    category=int(inputParams['category']),
                    name=inputParams['name'],
                    regions=inputParams['regions'],
                    address=inputParams['address'],
                    service_modes=inputParams['service_modes'],
                    contact=inputParams['contact'],
                    phoneno=inputParams['phoneno'],
                    cellphone=inputParams['cellphone'],
                    postcode=inputParams['postcode'],
                    swipeshow_album = int(inputParams['swipeshow_album']),
                    products_album = int(inputParams['products_album']),
                    longitude = float(inputParams['longitude']),
                    latitude = float(inputParams['latitude']),
                    specials = inputParams['specials'],
                ).where(Products.id == productId)
            q.execute()
        except Exception, e:
            return self.error(msg = '产品编辑失败: %s' % e, url=self.makeUrl('/admin/products/list'))

        return self.success('产品编辑成功', url=self.makeUrl('/admin/products/list'))

    def map(self):
        return self.display('map_select_widget')


    def add(self):

        userName = self.isLogin()
        user = Users.get(Users.name == userName)
        if not user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/products/list'))

        categoriesList = Categories.select()
        self.privData['CATEGORIES_LIST'] = categoriesList

        albumsList = Albums().select().where(Albums.owner == user.id)
        self.privData['ALBUMS_LIST'] = albumsList
        imagesList = Images().select().where(Images.owner == user.id)


        self.privData['USER'] = user
       
        groupsList = Groups().select().where(Groups.owner == user.id)
        #先创建一个公司，如果不存在公司，则需要先创建公司
        if not groupsList.count():
            return self.error(msg = '请先创建一个公司!', url=self.makeUrl('/admin/products/list'))
        self.privData['GROUPS_LIST'] = groupsList

        # 构建{album: images}, 同时排除不包括任何图片的专辑
        album_images_map = {}
        excluded_albums = []
        for album in albumsList:
            album_images = imagesList.where(Images.album == album.id)
            if album_images.count():
                album_images_map[album.id] = album_images
            else:
                excluded_albums.append(album.id)

        if imagesList.count():
            self.privData['ENABLE_SELECT_THUMBNAIL'] = True
            self.privData['ALBUMS_LIST'] = \
                [album for album in albumsList if album.id not in excluded_albums]
            self.privData['IMG_ALBUMS_LIST'] = album_images_map
            self.privData['CURRENT_ALBUM'] = self.privData['ALBUMS_LIST'][0]
            # 默认图片为默认专辑的第一张图片
            self.privData['CURRENT_IMG'] = album_images_map[self.privData['CURRENT_ALBUM'].id][0]
            self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('productAdd')


    def save(self):
        inputParams= self.getInput()
        userName = self.isLogin()
        user = Users.get(Users.name == userName)

        try:
            price = float(inputParams['price'])
            discount = float(inputParams['discount'])
        except ValueError as ve:
            raise Exception("价格或折扣格式有误，需要是数字")
        try:
            inputParams['longitude'] = inputParams['longitude'] if inputParams['longitude'] else 116.397428
            inputParams['latitude'] = inputParams['latitude'] if inputParams['latitude'] else 39.90923
            Products.create(
                name = inputParams['name'],
                regions = inputParams['regions'],
                price = price,
                discount = discount,
                description = self.htmlunquote(inputParams['description']),
                team_description = self.htmlunquote(inputParams['team_description']),
                owner = user.id,
                category = int(inputParams['category']),
                group = int(inputParams['group']),
                thumbnail = int(inputParams['thumbnail']),
                longitude = float(inputParams['longitude']),
                latitude = float(inputParams['latitude']),
                address = inputParams['address'],
                contact = inputParams['contact'],
                phoneno = inputParams['phoneno'],
                cellphone = inputParams['cellphone'],
                faxno = inputParams['faxno'],
                postcode = inputParams['postcode'],
                service_modes = inputParams['service_modes'],
                specials = inputParams['specials'],
                swipeshow_album = int(inputParams['swipeshow_album']),
                products_album = int(inputParams['products_album'])
              )
        except Exception, e:
            print e
            return self.error(msg = '新增产品失败: %s' % e, url=self.makeUrl('/admin/products/list'))

        return self.success('新增产品成功', url=self.makeUrl('/admin/products/list'))


    def comments(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
        ###评论是都能看到
        productCommentList = ProductComments.select()
        pageString = self.getPageStr('/admin/products/comments', page, count, productCommentList.count())
        self.privData['PRODUCTCOMM_LIST'] = productCommentList.paginate(page, config.COUNT_PER_PAGE)
        self.privData['PAGE_STRING'] = pageString

        return self.display('productcommViewList')


    def commupdate(self):
        inputParams= self.getInput()
        productcomm = ProductComments.get(ProductComments.id == int(inputParams['id']))

        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != productcomm.owner.id and not self.isAdmin():
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/products/list'))

        try:
            productcomm.content = inputParams['content']
            ##现在时间没有更新，需要更新时间为当前时间
            productcomm.save()
        except Exception, e:
            return self.error(msg = '产品评论修改失败: %s' % e, url=self.makeUrl('/admin/products/comments'))

        return self.success('产品评论修改成功!', url=self.makeUrl('/admin/products/comments'))

    def commdelete(self):
        inputParams = self.getInput()
        productcomm = ProductComments.get(ProductComments.id == int(inputParams['id']))
        

        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != productcomm.owner.id and not self.isAdmin() or not current_user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/products/comments'))

        try:
            productcomm.delete_instance()
        except Exception, e:
            return self.success(msg='产品评论删除失败: %s' % e, url=self.makeUrl('/admin/products/comments'))

        return self.success(msg='产品评论删除成功', url=self.makeUrl('/admin/products/comments'))

    def favorite(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
###favotar只有admin能看到全部的，否则只能看到本人的
        current_user = Users.get(Users.name == self.isLogin())
        productFavList = ProductFavorites.select()
        if not self.isAdmin():
            productFavList = productFavList.where(ProductFavorites.owner == current_user.id)
        pageString = self.getPageStr('/admin/products/favorites', page, count, productFavList.count())
        self.privData['PRODUCTFAV_LIST'] = productFavList.paginate(page, config.COUNT_PER_PAGE)
        self.privData['PAGE_STRING'] = pageString

        return self.display('productfavViewList')

    def favdelete(self):
        inputParams = self.getInput()
        productfav = ProductFavorites.get(ProductFavorites.id == int(inputParams['id']))

        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != productfav.owner.id and not self.isAdmin() or not current_user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/products/favorites'))

        try:
            productfav.delete_instance()
        except Exception, e:
            return self.success(msg='产品收藏删除失败: %s' % e, url=self.makeUrl('/admin/products/favorites'))

        return self.success(msg='产品收藏删除成功', url=self.makeUrl('/admin/products/favorites'))

    def ranklist(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
###打分是都能看到
        productRankList = ProductRankings.select().order_by(ProductRankings.id.desc())
        pageString = self.getPageStr('/admin/products/ranklist', page, count, productRankList.count())
        self.privData['PRODUCTRANK_LIST'] = productRankList.paginate(page, config.COUNT_PER_PAGE)
        self.privData['PAGE_STRING'] = pageString

        return self.display('productrankViewList')

    def rankdelete(self):
        inputParams = self.getInput()
        productrank = ProductRankings.get(ProductRankings.id == int(inputParams['id']))

        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != productrank.owner.id and not self.isAdmin() or not current_user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/products/ranklist'))

        try:
            productrank.delete_instance()
        except Exception, e:
            return self.error(msg='产品评价删除失败: %s' % e, url=self.makeUrl('/admin/products/ranklist'))

        return self.success(msg='产品评价删除成功', url=self.makeUrl('/admin/products/ranklist'))

    def videos(self):
        inputParams = self.getInput()

        try:
            import aodianyun
            productId = int(inputParams['id'])

            product = Products.get(Products.id == productId)
            current_user = Users.get(Users.name == self.isLogin())
            if current_user.id != product.owner.id and not self.isAdmin() or not current_user.role.type < 100:
                return self.error(msg = '权限不足!', url=self.makeUrl('/admin/products/list'))
        
            vods = aodianyun.Apis().get_upload_vod_list()
            self.privData['VIDEOS_LIST'] = vods['List']
            self.privData['PRODUCT'] = product
            return self.display('productLink')
        except Exception, e:
            return self.error(msg='关联视频失败: %s' % e, url=self.makeUrl('/admin/products/list'))

    def link(self):
        inputParams= self.getInput()  
        productId = inputParams['id']
        videoId = inputParams['sel']

        try:
            product = Products.get(Products.id == productId)
            current_user = Users.get(Users.name == self.isLogin())
            if current_user.id != product.owner.id and not self.isAdmin() or not current_user.role.type < 100:
                return self.error(msg = '权限不足!', url=self.makeUrl('/admin/products/list'))

            import aodianyun
            vods = aodianyun.Apis().get_upload_vod_list()['List']
            for vod in vods:
                if vod['id'] == videoId:
                    if vod.has_key('url'):
                        product.video_url=vod['url']
                    if vod.has_key('title'):
                        product.video_name=vod['title']
                    if vod.has_key('desc'):
                        product.video_desc=vod['desc']
                    if vod.has_key('m3u8_240'):
                        product.video_mobile_url=vod['m3u8_240']
                    if vod.has_key('adaptive'):
                        product.video_adaptive_url=vod['adaptive']
                    if vod.has_key('videoRate'):
                        product.video_rate=vod['videoRate']
                    if vod.has_key('width'):
                        product.video_width=vod['width']
                    if vod.has_key('height'):
                        product.video_height=vod['height']
                    if vod.has_key('thumbnail'):
                        product.video_thumbnail=vod['thumbnail']
                    if vod.has_key('uptime'):
                        product.video_uptime=vod['uptime']
                    if vod.has_key('duration'):
                        product.video_duration=vod['duration']
                    product.save()
        except Exception, e:
            return self.error(msg='关联视频失败: %s' % e, url=self.makeUrl('/admin/products/list'))

        return self.success('关联视频成功', url=self.makeUrl('/admin/products/list'))

 
