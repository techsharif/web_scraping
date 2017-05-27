def content_between_string(string, start, end):
    data = []
    start_pos = 0
    while (1):
        start_pos = string.find(start, start_pos)
        if start_pos == -1:
            break
        start_pos += len(start)
        end_pos = string.find(end, start_pos)
        if end_pos == -1:
            break

        data += [string[start_pos:end_pos]]
    return data


def just_get_digits(st):
    s = ""
    for i in st:
        if i.isdigit() or i=='.':
            s+=i
    return s

def generate_html(data, total):
    str_top = '''<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <style>
        .main {
            width: 1000px;
            margin: 0 auto;
            padding: 10px;
        }

        table {
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
        }

        td, th {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }

        tr:nth-child(even) {
            background-color: #dddddd;
        }
    </style>
</head>
<body>
<div class="main">
    <h2>Online Shopping</h2>
    <table>
    <tr>
        <th>Image</th>
        <th>Description</th>
        <th>Price</th>
    </tr>'''
    s = ""
    for d in data:
        s += "<tr>"
        s += '<td><img src="' + d['image'] + '"></td>'
        s += '<td>' + d['title'] + '</td>'
        s += '<td>$' + d['price'] + '</td>'
        s += "</tr>"
    s += "<tr>"
    s += '<td></td>'
    s += '<td>Total</td>'
    s += '<td>$' + str(total) + '</td>'
    s += "</tr>"

    str_btm = '''
        </table>
</div>
</body>
</html>
    '''

    file = open('invoice.html', 'w')
    file.write(str_top + s + str_btm)
    file.close()
