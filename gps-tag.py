from pexif import JpegFile
import sys
import os
import glob

jpgFile = "test"
gpxFile = "plymouth.gpx"

offset = 500

srcRep = "\\uk\\Photos"
dstRep = "\\uk\\Python\\Exif\\fixed"

try:
    for jpgFile in glob.glob(srcRep+'\\*.jpg'):
        print "Traitement de " + jpgFile
        try:
            ef = JpegFile.fromFile(jpgFile)

            primary = ef.get_exif().get_primary()
            dt = primary.ExtendedEXIF.DateTimeOriginal[:10]
            dt = dt.replace(":","-")

            tm = primary.ExtendedEXIF.DateTimeOriginal[11:]
            tm = tm.split(":")

            # dans le JPEG, 12h heure FR = 13h heure UK

            j_hr=int(tm[0])
            j_mn=int(tm[1])
            j_sc=int(tm[2])

            # il y a 500 s d'ecart entre heure GPS et heure GPS

            j_time = (j_hr*3600) + (j_mn*60) + j_sc + offset

            posLat = 0
            posLon = 0
            diffTime = 4*3600

            for gpxLine in open(gpxFile, 'r'):
                if "<trkpt " in gpxLine:
                    gpxPos = gpxLine
                if (dt in gpxLine):
                    # Un point trouv? ? la bonne date : chercher si il est
                    # plus proche en temps du dernier trouv?
                    # dans le gpx, 12h heure FR = 13h heure UK
                    gpxLine = gpxLine.strip()
                    g_hr=int(gpxLine[17:19])
                    g_mn=int(gpxLine[20:22])
                    g_sc=int(gpxLine[23:25])
                    g_time = (g_hr*3600) + (g_mn*60) + g_sc

                    if (abs(j_time - g_time) < diffTime):
                        diffTime = abs(j_time - g_time)
                        latlon = gpxPos.split('\"')
                        posLat = latlon[1]
                        posLon = latlon[3]
            if ((posLat==0) and (posLon==0)):
                print "   => pas de position trouv?e ? cette heure"
            else:
                # Ecriture du tag GPS dans l'EXIF de la photo avec les
                # meilleures lat/lon trouv?es

                ef.set_geo(float(posLat), float(posLon))
                print "   => diffTime=",diffTime

                base=os.path.basename(jpgFile)
                print "   => Enregistre sous : " + dstRep + "\\" + base
                ef.writeFile(dstRep + "\\" + base)
            print "   => ok"
        except:
            print "   => FAILED"

except IOError:
   type, value, traceback = sys.exc_info()
   print >> sys.stderr, "Error saving file:", value
