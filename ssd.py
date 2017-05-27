import urllib2
import test


def get_ssds(numbers):
    response = urllib2.urlopen('https://www.newegg.com/Product/ProductList.aspx?Submit=Property&Subcategory=636&N=100011693%20600488413%20601193225%20601193224%204814&IsNodeId=1&IsPowerSearch=1&cm_sp=CAT_SSD_2-_-VisNav-_-M.2_1')
    html = str(response.read())
    data = test.content_between_string(html,'class="item-container','"price-save"')
    ssds = []
    for d in data:
        try:
            image = 'http://'+test.content_between_string(d,'src="//','"')[0]
            title = test.content_between_string(d,'title="','"')[0]
            price = test.content_between_string(d,'</span>$<strong>','</strong>')[0]
            ssds += [{
                'title':title,
                'image':image,
                'price':price
            }]
        except:
            print 'error in' + d

    return ssds[-numbers:]
