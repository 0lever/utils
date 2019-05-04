# -*- coding:utf-8 -*-
import oss2


class Oss(object):
    def __init__(self, access_key_id, access_key_secret, endpoint, bucket_name):
        auth = oss2.Auth(access_key_id, access_key_secret)
        self._endpoint = endpoint
        self._bucket_name = bucket_name
        self._bucket = oss2.Bucket(auth, endpoint, bucket_name)

    def upload(self, src_path, dst_path):
        self._bucket.put_object_from_file(dst_path, src_path)
        return self._get_oss_url(dst_path)

    def upload_data(self, data, dst_path):
        self._bucket.put_object(dst_path, data)
        return self._get_oss_url(dst_path)

    def append_data(self, data, dst_path):
        try:
            oss_file = self._get_oss_object(dst_path)
            position = oss_file.content_length
        except oss2.exceptions.NoSuchKey:
            self._bucket.object_exists(dst_path)
            position = 0
        except:
            raise
        self._bucket.append_object(position=position, key=dst_path, data=data)
        return self._get_oss_object(dst_path)

    def delete(self, dst_path):
        return self._bucket.delete_object(dst_path)

    def _get_oss_url(self, dst_path):
        return "https://%s.%s/%s" % (self._bucket_name, self._endpoint.split("//")[-1], dst_path)

    def _get_oss_object(self, dst_path):
        return self._bucket.get_object(dst_path)