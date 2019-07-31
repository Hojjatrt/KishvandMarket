import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def resize(low_pic, high_pic, size=(300, 300), size2=None, quality=100):

    low_img = Image.open(low_pic)
    high_img = Image.open(low_pic)
    output = BytesIO()
    output2 = BytesIO()
    ext = low_pic.name.split('.')[1]

    #The image is scaled/cropped vertically or horizontally depending on the ratio
    # if low_img.size[0] > size[0] and low_img.size[1] > size[1]:
    #     high_img = high_img.resize((size[0],size[1]),
    #             Image.ANTIALIAS)

    # high_img = high_img.resize((size[0], size[1]), Image.ANTIALIAS)
    low_img = low_img.resize(size, Image.ANTIALIAS)
    if size2 is not None:
        high_img = high_img.resize(size2, Image.ANTIALIAS)

    if ext == 'png' or ext == 'PNG':
        low_img.save(output, format='PNG', quality = quality)
        output.seek(0)
        low_pic = InMemoryUploadedFile(output, 'ImageField',
                                            "%s.png" % low_pic.name.split('.')[0],
                                            'image/png', sys.getsizeof(output), None)

        high_img.save(output2, format='PNG', quality = quality)
        output2.seek(0)
        high_pic = InMemoryUploadedFile(output2, 'ImageField',
                                       "%s.png" % low_pic.name.split('.')[0],
                                       'image/png', sys.getsizeof(output2), None)
    elif ext == 'jpg' or ext == 'JPEG' or ext == 'JPG' or ext == 'jpeg':
        low_img.save(output, format='JPEG', quality = quality)
        output.seek(0)
        low_pic = InMemoryUploadedFile(output, 'ImageField',
                                            "%s.jpg" % low_pic.name.split('.')[0],
                                            'image/jpeg', sys.getsizeof(output), None)

        high_img.save(output2, format='JPEG', quality = quality)
        output2.seek(0)
        high_pic = InMemoryUploadedFile(output2, 'ImageField',
                                       "%s.jpg" % low_pic.name.split('.')[0],
                                       'image/jpeg', sys.getsizeof(output2), None)
    else:
        low_img.save(output)
        high_img.save(output2)

    return (low_pic , high_pic)