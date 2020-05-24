from pexif import JpegFile
import sys
import os
import glob

photoRep = "e:\\uk\\Python\\seb\\photos"
logFile = photoRep + "\\gps-tag.csv"

SEP = ';'

try:
    fOut = open(logFile,"w")
    ligne = "Repertoire"    + SEP + \
            "Fichier"       + SEP + \
            "Date"          + SEP + \
            "Heure"         + SEP + \
            "Marque"        + SEP + \
            "Modele"        + SEP + \
            "Exposition"    + SEP + \
            "Aperture"      + SEP + \
            "Equiv ISO"     + SEP + \
            "Dim X"         + SEP + \
            "Dim Y"         + SEP + \
            "Latitude"      + SEP + \
            "Longitude"     + '\n'
    fOut.write(ligne)

    path = photoRep
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            jpgFile = os.path.join(dirname, filename)
            fext = os.path.splitext(jpgFile)[1]
            if fext.upper() == '.JPG':
                print "Traitement de " + jpgFile
            else:
                print "Ignore " + jpgFile
                continue

            try:
                ef = JpegFile.fromFile(jpgFile)

                primary = ef.get_exif().get_primary()
                dt = primary.ExtendedEXIF.DateTimeOriginal[:10]
                tm = primary.ExtendedEXIF.DateTimeOriginal[11:]

                try:
                    GPSpos = ef.get_geo()
                except:
                    GPSpos = (0,0)

                exifTags = primary.entries
                exifExtended = primary.ExtendedEXIF.entries
                for tag in exifTags :
                    if tag[0] == 0x10F:
                       xf_Marque = tag[2]
                    if tag[0] == 0x110:
                       xf_Model = tag[2]
                    if tag[0] == 0x9201:
                       xf_Model = tag[2]

                xf_DimX     = "error"
                xf_DimY     = "error"
                xf_Exposure = "error"
                xf_Aperture = "error"
                xf_Iso      = "error"
                try:
                   xf_DimX     = str(primary.ExtendedEXIF.PixelXDimension[0])
                   xf_DimY     = str(primary.ExtendedEXIF.PixelYDimension[0])
                   xf_Exposure = str(primary.ExtendedEXIF.ExposureTime[0])
                   xf_Aperture = str(primary.ExtendedEXIF.MaxApertureValue[0])
                   xf_Iso      = str(primary.ExtendedEXIF.ISOSpeedRatings[0])
                except:
                   print "   => EXIF fields error"

                ligne = dirname                        + SEP + \
                        os.path.basename(jpgFile)      + SEP + \
                        dt                             + SEP + \
                        tm                             + SEP + \
                        xf_Marque                      + SEP + \
                        xf_Model                       + SEP + \
                        xf_Exposure                    + SEP + \
                        xf_Aperture                    + SEP + \
                        xf_Iso                         + SEP + \
                        xf_DimX                        + SEP + \
                        xf_DimY                        + SEP + \
                        str(GPSpos[0])                 + SEP + \
                        str(GPSpos[1])                 + '\n'

                fOut.write(ligne)
                print "   => "+ligne
            except:
                print "   => FAILED"
    fOut.close()
except IOError:
    type, value, traceback = sys.exc_info()
    print >> sys.stderr, "Error parsing files"
