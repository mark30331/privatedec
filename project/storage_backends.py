try:
    from storages.backends.s3 import S3Storage
except ImportError:  # pragma: no cover
    from storages.backends.s3boto3 import S3Boto3Storage as S3Storage


class PrivateR2MediaStorage(S3Storage):
    default_acl = None
    file_overwrite = False
    querystring_auth = True
    custom_domain = None

    def get_available_name(self, name, max_length=None):
        return name
