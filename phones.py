import urllib2
import test


def get_phones(numbers):
    response = urllib2.urlopen('https://www.kogan.com/au/shop/phones/')
    html = str(response.read())
    data = test.content_between_string(html,'class="product-item"','</article>')
    phones = []
    for d in data:
        try:
            image = test.content_between_string(d,'src="','"')[0]
            title = test.content_between_string(d,'title="','"')[0]
            price = test.content_between_string(d,'$','<')[0]
            phones += [{
                'title':title,
                'image':image,
                'price':price
            }]
        except:
            print 'error in' + d

    return phones[-numbers:]
