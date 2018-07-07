import os
from PIL import Image
from PIL import ExifTags
import piexif
import numpy as np
# install pillow and piexif

#tutorial:
#https://support.google.com/fusiontables/answer/1244603?hl=en
thedir = 'photos'
f = open("output.csv","w")
def exif_to_degrees(value):
    A = np.array(value, dtype=float)
    m,n = A.shape
    assert (m,n) == (3,2), 'require a triple of pairs'
    return (A[:,0] / A[:,1]).dot(
        np.array([60.**(-i) for i in xrange(3)]))


for filename in os.listdir(thedir):
    if filename.split('.')[-1] not in ['jpg', 'JPG']:
        continue
    
    try:
        im = Image.open(os.path.join(thedir, filename))
        gps = piexif.load(im.info['exif'])['GPS']
        gps = { ExifTags.GPSTAGS[i]:gps[i] for i in gps }

        if len(gps) == 0:
            print filename, 'has empty GPS info'
            continue

        if len({'GPSLatitude', 'GPSLongitude', 'GPSTimeStamp'
               }.intersection(gps.keys())) < 3:
            print filename, 'missing GPS space-time tags'
            continue
        
        gps['GPSLatitude'] = exif_to_degrees(gps['GPSLatitude'])
        gps['GPSLongitude'] = exif_to_degrees(gps['GPSLongitude'])
        gps['GPSTimeStamp'] = ':'.join(
            [str(a) for a,b in gps['GPSTimeStamp']]) + 'Z'

        spacetime = '{}{},{}{},{},{}'.format(
            '' if gps['GPSLatitudeRef'] == 'N' else '-',
            gps['GPSLatitude'],
            '' if gps['GPSLongitudeRef'] == 'E' else '-',
            gps['GPSLongitude'],
            gps['GPSDateStamp'],
            gps['GPSTimeStamp'])
        f.write(filename+","+spacetime+"\n")


    except IOError:
        print filename, 'had IO Error'

    except KeyError:
        assert 'exif' not in im.info
        print filename, 'has no EXIF data'

    except ValueError:
        print filename, 'crashes on parsing EXIF data'
        
    except:
        print filename, 'has general processing failure'
        raise
f.close()
