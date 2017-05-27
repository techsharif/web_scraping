import urllib2
import test


def get_digital_cameras(numbers):
    response = urllib2.urlopen('http://www.shopzilla.com/digital-cameras/402/products')
    html = str(response.read())
    # print str(html)
    data = test.content_between_string(html,'<table class="offer result">','</table>')
    digital_cameras = []
    for d in data:
        try:
            image = test.content_between_string(d,'width="75" height="75" src="','"')[0].replace('&amp;','&')
            title = test.content_between_string(d,'title="','"')[0]
            price = test.content_between_string(d,'$','.')[0]
            digital_cameras += [{
                'title':title,
                'image':image,
                'price':price
            }]
        except:
            print 'error in' + d
    return digital_cameras[-numbers:]

