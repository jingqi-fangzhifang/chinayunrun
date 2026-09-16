#!/usr/bin/python
# encoding=utf-8
"""
电信 CTWing(AEP) 开放平台 Python SDK —— 产品管理模块
文件对应官方 SDK 的 apis/aep_product_management.py

QueryProduct     产品详情：GET /aep_product_management/product      version 20181031202055
QueryProductList 产品列表：GET /aep_product_management/products     version 20190507004824
注意：这两个查询接口只需要应用级鉴权（appKey/appSecret），不需要 MasterKey。

QueryProductByImei 为本地扩展（非官方 SDK 内容）：只给 appKey/appSecret/imei 三个参数，
反查出该 IMEI 对应的产品。见文件末尾「本地扩展」区块。
"""
try:
    from . import AepSdkRequestSend
except (ImportError, ValueError):
    import AepSdkRequestSend

# 同一路径 /product 下按 HTTP 方法区分接口，version 各不相同
#   GET    /product  查询产品详情  20181031202055
#   POST   /product  创建产品      20191018204154
#   PUT    /product  修改产品      20191018204806
#   DELETE /product  删除产品      20181031202029
VERSION_PRODUCT_QUERY = '20181031202055'
VERSION_PRODUCT_LIST = '20190507004824'


def QueryProduct(appKey, appSecret, productId):
    """查询单个产品详情"""
    path = '/aep_product_management/product'
    head = {}
    param = {'productId': productId}
    version = VERSION_PRODUCT_QUERY
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, None, version,
                                                application, None, key, 'GET')
    if response is not None:
        return response.read()
    return None


def QueryProductList(appKey, appSecret, searchValue, pageNow, pageSize):
    """查询产品列表"""
    path = '/aep_product_management/products'
    head = {}
    param = {'searchValue': searchValue, 'pageNow': pageNow, 'pageSize': pageSize}
    version = VERSION_PRODUCT_LIST
    application = appKey
    key = appSecret
    response = AepSdkRequestSend.sendSDKRequest(path, head, param, None, version,
                                                application, None, key, 'GET')
    if response is not None:
        return response.read()
    return None


# ==================== 本地扩展（非官方 SDK 内容） ====================
# 平台没有「用 IMEI 直接查产品」的接口（官方 SDK 里也没有 QueryProductByImei），
# 所以这里用两个已有接口拼出这个能力，入口是 QueryProductByImei，只吃 3 个参数。
import json

try:
    from concurrent.futures import ThreadPoolExecutor
except ImportError:          # Python2 兼容：退化为串行
    ThreadPoolExecutor = None

try:
    from . import aep_device_management
except (ImportError, ValueError):
    import aep_device_management

SCAN_WORKERS = 6             # IMEI 反查时的并发线程数，改成 1 即串行
PRODUCT_PAGE_SIZE = 100      # 产品列表接口每页上限就是 100，传更大也只会返回 100


def _listAllProducts(appKey, appSecret):
    """拉取应用下全部产品（自动翻页）"""
    products = []
    pageNow = 1
    while True:
        raw = QueryProductList(appKey, appSecret, '', pageNow, PRODUCT_PAGE_SIZE)
        if not raw:
            break
        data = json.loads(raw.decode('utf-8'))
        items = (data.get('result') or {}).get('list') or []
        products.extend(items)
        if len(items) < PRODUCT_PAGE_SIZE:
            break
        pageNow += 1
    return products


def _probeProduct(appKey, appSecret, product, imei):
    """在单个产品下按 IMEI 查设备列表

    返回 (product, device, error)：
        device 为 dict  -> 在该产品下查到了这台设备
        device 为 None  -> 该产品下没有这个 IMEI（error 也为 None）
        error  非空     -> 该产品查询报错，跳过即可
    """
    try:
        raw = aep_device_management.QueryDeviceList(
            appKey, appSecret, product.get('apiKey'),
            product.get('productId'), imei, 1, 1)
        data = json.loads(raw.decode('utf-8')) if raw else {}
        result = data.get('result') or {}
        if (result.get('total') or 0) > 0:
            return product, (result.get('list') or [{}])[0], None
        return product, None, None
    except Exception as e:
        return product, None, str(e)


def QueryProductByImei(appKey, appSecret, imei):
    """通过 IMEI 反查它对应的产品（只需应用级参数 appKey / appSecret）

    平台侧没有这种接口，实现思路：
      1) 用产品列表接口（应用级鉴权）拉取应用下全部产品。返回结果里每个产品的
         apiKey 字段就是该产品的 Master-APIkey，所以不必再手工维护 productId 对照表；
      2) 逐个产品调设备列表接口，用 searchValue=IMEI 精确匹配。命中的那个产品就是答案。

    参数：
        appKey/appSecret —— 控制台「应用管理」里的 App Key / App Secret
        imei             —— 15 位 IMEI 字符串

    返回 dict：
        {
          'imei':        输入的 IMEI,
          'found':       是否查到,
          'productId':   产品 ID（未查到为 None）,
          'productName': 产品名称（未查到为 None）,
          'deviceId':    设备 ID，32 位十六进制（未查到为 None）,
          'deviceName':  设备名称,
          'matched':     命中的产品 [(productId, productName), ...]，正常只有 1 条,
          'scanned':     实际扫描的产品数,
          'errors':      扫描中出错的产品 [(productId, 错误信息), ...]，正常为空,
        }

    耗时：产品列表约 0.6 秒；命中一般 1~3 秒返回；全部产品扫完仍未命中约 10 秒。
    注意：只能查到「本应用可见」的产品，若该 IMEI 所属产品不在产品列表里则查不到。
    """
    imei = str(imei).strip()
    products = _listAllProducts(appKey, appSecret)
    # 设备数多的产品先扫，常见 IMEI 往往靠前就命中
    products.sort(key=lambda p: -(p.get('deviceCount') or 0))

    hits, errors = [], []

    def collect(product, device, error):
        if error:
            errors.append((product.get('productId'), error))
        elif device is not None:
            hits.append((product, device))

    if ThreadPoolExecutor is not None and SCAN_WORKERS > 1 and len(products) > 1:
        with ThreadPoolExecutor(max_workers=SCAN_WORKERS) as pool:
            for product, device, error in pool.map(
                    lambda p: _probeProduct(appKey, appSecret, p, imei), products):
                collect(product, device, error)
    else:
        for p in products:
            collect(*_probeProduct(appKey, appSecret, p, imei))

    result = {
        'imei': imei,
        'found': bool(hits),
        'productId': None,
        'productName': None,
        'deviceId': None,
        'deviceName': None,
        'matched': [(p.get('productId'), p.get('productName')) for p, _ in hits],
        'scanned': len(products),
        'errors': errors,
    }
    if hits:
        product, device = hits[0]
        result['productId'] = product.get('productId')
        result['productName'] = product.get('productName')
        result['deviceId'] = device.get('deviceId')
        result['deviceName'] = device.get('deviceName')
    return result

if __name__ == '__main__':
    print(QueryProductByImei('rir7vzEpGMc', 'JCI01Nm0B0', '862447066252065'))