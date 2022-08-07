
import requests
from pprint import pprint
from datetime import date

token_ya = ""
token_vk = ""
user_id = ""


def uploading_photos(id, album = "profile"):
    url = "https://api.vk.com/method/photos.get/"
    params = {'access_token': token_vk, 'owner_id': id, 'album_id': album, 'photo_sizes': '1', 'v': '5.131', 'extended':1}
    res = requests.get(url, params = params)
    res = res.json()
    res = res["response"]["items"]
    photo_parameters = {}
    for photo in res:
        name_photo = photo["likes"]["count"]
        for size in photo["sizes"]:
            if size['type'] == 'z':
                url_photo = size['url']
        if name_photo in photo_parameters:
            date_photo = date.fromtimestamp(photo["date"])
            name_photo = (f'{photo["likes"]["count"]}_{date_photo}')
        else:
            name_photo = photo["likes"]["count"]
        photo_parameters[name_photo] = url_photo
    return(photo_parameters)

class YaUploader:
   def __init__(self):
       pass
   def download_file (self, token):
       upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
       headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}
       params = {"path":"netology/photos", "overwrite": "True"}
       folder_path = requests.put(upload_url, headers=headers, params=params)
       upload_url_download = "https://cloud-api.yandex.net/v1/disk/resources/upload"
       list_download = {}
       for id, (name_photos, url_foto) in enumerate(uploading_photos(user_id).items(), 1):
           path_download = (f'netology/photos/{name_photos}.png')
           params_download = {"path": path_download, "url": url_foto}
           download = requests.post(upload_url_download, headers=headers, params=params_download)
           if download.status_code == 202:
               print(f"Загружено фото № {id} из {len(uploading_photos(user_id))}")
               download_json = download.json()
               list_download[name_photos] = download_json
           else:
               print (f"Ошибка загрузки, код ошибки {download.status_code}")

       return pprint(list_download)


if __name__ == '__main__':
    download_foto = YaUploader()
    result = download_foto.download_file(token_ya)

