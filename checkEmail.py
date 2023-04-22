def check(email):
    data = [{
        'email': '2020ceb1004@iitrpr.ac.in',
        'username': 'Aman',
        'id': 1,
        },
            {
        'email': '2020ceb1005@iitrpr.ac.in',
        'username': 'Aman Kumar',
        'id': 2,
        'isAdmin': True
        },
            {
        'email': '2020ceb1017@iitrpr.ac.in',
        'username': 'Lakshay Bansal',
        'id': 3,
        }
    ]
    out = list(filter(lambda item: item['email'] == email, data))
    if (len(out)):
        return out[0]
    return False 

email = '2020ceb1005@iitrpr.ac.in'
# print(check(email))
