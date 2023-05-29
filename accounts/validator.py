from django.core.exceptions import ValidationError
import os




def allow_only_images_validator(value):
    ext=os.path.splitext(value.name)[1]
    print(ext)
    valid_extensions=['.png','.jpg','.jpeg']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unssupported file extention. Allowed extensions : '+ str(valid_extensions))