from django.conf import settings
from django.core.files.storage import Storage
import cloudinary
import cloudinary.uploader
import cloudinary.api


class Cloudinary(Storage):
    def __init__(self):
        self.directory = settings.CLOUDINARY_DIRECTORY

    def upload(self, file):
        # Upload the file to Cloudinary
        response = cloudinary.uploader.upload(file, folder=self.directory)
        return response

    def delete(self, public_id):
        # Delete the file from Cloudinary
        result = cloudinary.api.delete_resources([public_id])

        # Return True if the deletion was successful
        return result["deleted"][public_id] == "deleted"

    def exists(self, name):
        try:
            cloudinary.api.resource(name)
            return True
        except:
            return False

    def url(self, name):
        return cloudinary.utils.cloudinary_url(name)[0]
