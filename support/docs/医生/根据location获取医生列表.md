# URL请求
```
http://47.106.101.39/v1/doctors/by_location
```

# 方法:
```
POST
```

# 参数：
```
province:  int，省份code，必带
city: int，城市code，可不带，不带表示拿省份
area: int，市区code，可不带，不带表示拿城市
page_num: int，分页页码
page_size: int，每页的size
```
# 请求体：
```
{
	"page_num": 1,
	"province": 0,
	"city": 0,
	"area": 0,
	"page_size": 6,
	"common_param": {
		"user_id": "",
		"cuid": "xxx-aaa-bbb-ccc",
		"device_type": "ios",
		"device_os": "ios_11.05",
		"app_version": "1.0.0",
		"channel": "offical",
        "sid": "fsAUFzMzV9DYS8lc6ldqtMNIP+d/CvmJKDmKpRM8xkOamOVReqRYnQ=="
	}
}
```
# 返回：
```
{
    "data": {
        "list": [
            {
                "area": 0,
                "avatar": "http://www.mingyihui.net/upload/photo/doctor/hKO2631476_image140.jpg",
                "channel": "",
                "city": 0,
                "comment_cnt": 25,
                "cookie": "",
                "create_time": "Sun, 19 Aug 2018 23:10:26 GMT",
                "csr": 96,
                "cuid": "1534691425_42161",
                "del_flag": 0,
                "device_model": "",
                "device_os": "",
                "device_type": "",
                "good_at": "乳腺癌 乳腺肿瘤 乳管内乳头状瘤 乳房导管内乳头状瘤 乳腺导管癌 ...",
                "hospital": "上海新华医院",
                "hospital_index": null,
                "id": 4,
                "like_cnt": 24,
                "number": 155,
                "phone": "",
                "positional_title": "副主任医师",
                "province": 0,
                "push_token": "",
                "register_ip": "",
                "section": "普外科",
                "section_code": 101,
                "sex": 1,
                "update_time": "Thu, 23 Aug 2018 08:00:16 GMT",
                "user_name": "宋和平",
                "version": "",
                "wxopenid": ""
            },
            {
                "area": 0,
                "avatar": "http://www.mingyihui.net/upload/images/doctor_default155x155.jpg",
                "channel": "",
                "city": 0,
                "comment_cnt": 1,
                "cookie": "",
                "create_time": "Sun, 19 Aug 2018 23:10:26 GMT",
                "csr": 100,
                "cuid": "1534691425_26845",
                "del_flag": 0,
                "device_model": "",
                "device_os": "",
                "device_type": "",
                "good_at": "重症肌无力 ...",
                "hospital": "卫生部北京医院",
                "hospital_index": null,
                "id": 1,
                "like_cnt": 1,
                "number": 311,
                "phone": "",
                "positional_title": "副主任医师",
                "province": 0,
                "push_token": "",
                "register_ip": "",
                "section": "胸外科",
                "section_code": 101,
                "sex": 1,
                "update_time": "Thu, 23 Aug 2018 08:00:07 GMT",
                "user_name": "王永忠",
                "version": "",
                "wxopenid": ""
            }
        ]
    },
    "msg": "ok",
    "ret": 0
}
```



