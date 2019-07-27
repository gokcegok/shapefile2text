"""
This program prepared for read shapefiles. A shapefile consists of a main file(.shp),
an index file(.shx), and a dBASE table.


Gokce GOK, 2019
"""


from struct import *
from collections import namedtuple
import os
from dbfread import DBF


BoundingBox = namedtuple('BoundingBox', 'xmin ymin xmax ymax zmin zmax mmin mmax')
RecordHeader = namedtuple('RecordHeader', 'number length')
ShapeBox = namedtuple('ShapeBox', 'xmin ymin xmax ymax')

def shp2txt(shape_path):
    # This function reads .shp file and prints all information to a .txt file.
    # Parameter: File name
    file_name = shape_path.split('.')[0]
    extension = '.txt'
    with open(shape_path, 'rb') as fp:
        with open(file_name + 'SHP' + extension, 'w') as shp:
            f_code, *_, f_length = unpack('>iiiiiii', fp.read(28))
            shp.write('File Code: ' + '\t' + str(f_code))
            shp.write('\n' + 'File Length: ' + '\t' + str(f_length))
            f_version, shape_type = unpack('<ii', fp.read(8))
            shp.write('\n' + 'Version :' + '\t' + str(f_version))
            shp.write('\n' + 'Shape Type: ' + '\t' + str(shape_type))
            boundingBox = BoundingBox._make(unpack('<dddddddd', fp.read(64)))
            shp.write('\n' + 'Xmin: ' + '\t' + str(boundingBox.xmin))
            shp.write('\n' + 'Ymin: ' + '\t' + str(boundingBox.ymin))
            shp.write('\n' + 'Xmax: ' + '\t' + str(boundingBox.xmax))
            shp.write('\n' + 'Ymax: ' + '\t' + str(boundingBox.ymax))
            shp.write('\n' + 'Zmin: ' + '\t' + str(boundingBox.zmin))
            shp.write('\n' + 'Zmax: ' + '\t' + str(boundingBox.zmax))
            shp.write('\n' + 'Mmin: ' + '\t' + str(boundingBox.mmin))
            shp.write('\n' + 'Mmax: ' + '\t' + str(boundingBox.mmax))
            if shape_type == 0: #Null
                while True:
                    try:
                        shp.write('\n')
                        record_number, content_length = unpack('>ii', fp.read(8))
                        shp.write('\n' + 'Record Number: ' + '\t' + str(record_number))
                        shp.write('\n' + 'Content Number: ' + '\t' + str(content_length))
                        shp_type = unpack('<i', fp.read(4))
                        shp.write('\n' + 'Shape Type: ' + '\t' + str(shp_type[0]))
                    except:
                        break
            if shape_type == 1: #Point
                while True:
                    try:
                        shp.write('\n')
                        record_number, content_length = unpack('>ii', fp.read(8))
                        shp.write('\n' + 'Record Number: ' + '\t' + str(record_number))
                        shp.write('\n' + 'Content Number: ' + '\t' + str(content_length))
                        shp_type = unpack('<i', fp.read(4))
                        shp.write('\n' + 'Shape Type: ' + '\t' + str(shp_type[0]))
                        shp.write('\n' + 'X: ' + '\t' + str(unpack('<d', fp.read(8))[0]))
                        shp.write('\n' + 'Y: ' + '\t' + str(unpack('<d', fp.read(8))[0]))
                    except:
                        break
            if shape_type == 3: #Polyline
                while True:
                    try:
                        shp.write('\n')
                        record_number, content_length = unpack('>ii', fp.read(8))
                        shp.write('\n' + 'Record Number: ' + '\t' + str(record_number))
                        shp.write('\n' + 'Content Number: ' + '\t' + str(content_length))
                        shp_type = unpack('<i', fp.read(4))
                        shp.write('\n' + 'Shape Type: ' + '\t' + str(shp_type[0]))
                        shapeBox = ShapeBox._make(unpack('<dddd', fp.read(32)))
                        shp.write('\n' + 'Xmin: ' + '\t' + str(shapeBox.xmin))
                        shp.write('\n' + 'Ymin: ' + '\t' + str(shapeBox.ymin))
                        shp.write('\n' + 'Xmax: ' + '\t' + str(shapeBox.xmax))
                        shp.write('\n' + 'Ymax: ' + '\t' + str(shapeBox.ymax))
                        n_parts, n_points = unpack('<ii', fp.read(8))
                        shp.write('\n' + 'Number of Parts: ' + '\t' +str(n_parts))
                        shp.write('\n' + 'Total Number of Points' + '\t' + str(n_points))
                        parts = unpack('<' + ''.join(['i'] * n_parts), fp.read(n_parts * 4))
                        shp.write('\n' + "Index List Part's First Points: " + str(parts))
                        points = unpack('<' + ''.join(['dd'] * n_points), fp.read(n_points * 16))
                        shp.write('\n' + 'Coordinates of Points(X, Y): ')
                        for i in range(0, len(points)-1, 2):
                            shp.write('\n' + str(points[i]) + ', ' + str(points[i+1]))
                    except:
                        break
            if shape_type == 5: #Polygon
                while True:
                    try:
                        shp.write('\n')
                        record_number, content_length = unpack('>ii', fp.read(8))
                        shp.write('\n' + 'Record Number: ' + '\t' + str(record_number))
                        shp.write('\n' + 'Content Number: ' + '\t' + str(content_length))
                        shp_type = unpack('<i', fp.read(4))
                        shp.write('\n' + 'Shape Type: ' + '\t' + str(shp_type[0]))
                        shapeBox = ShapeBox._make(unpack('<dddd', fp.read(32)))
                        shp.write('\n' + 'Xmin: ' + '\t' + str(shapeBox.xmin))
                        shp.write('\n' + 'Ymin: ' + '\t' + str(shapeBox.ymin))
                        shp.write('\n' + 'Xmax: ' + '\t' + str(shapeBox.xmax))
                        shp.write('\n' + 'Ymax: ' + '\t' + str(shapeBox.ymax))
                        n_parts, n_points = unpack('<ii', fp.read(8))
                        shp.write('\n' + 'Number of Parts: ' + '\t' +str(n_parts))
                        shp.write('\n' + 'Total Number of Points' + '\t' + str(n_points))
                        parts = unpack('<' + ''.join(['i'] * n_parts), fp.read(n_parts * 4))
                        shp.write('\n' + "Index List Part's First Points: " + str(parts))
                        points = unpack('<' + ''.join(['dd'] * n_points), fp.read(n_points * 16))
                        shp.write('\n' + 'Coordinates of Points(X, Y): ')
                        for i in range(0, len(points) - 1, 2):
                            shp.write('\n' + str(points[i]) + ', ' + str(points[i + 1]))
                    except:
                        break
            if shape_type == 8: #Multipoint
                while True:
                    try:
                        shp.write('\n')
                        record_number, content_length = unpack('>ii', fp.read(8))
                        shp.write('\n' + 'Record Number: ' + '\t' + str(record_number))
                        shp.write('\n' + 'Content Number: ' + '\t' + str(content_length))
                        shp_type = unpack('<i', fp.read(4))
                        shp.write('\n' + 'Shape Type: ' + '\t' + str(shp_type[0]))
                        shapeBox = ShapeBox._make(unpack('<dddd', fp.read(32)))
                        shp.write('\n' + 'Xmin: ' + '\t' + str(shapeBox.xmin))
                        shp.write('\n' + 'Ymin: ' + '\t' + str(shapeBox.ymin))
                        shp.write('\n' + 'Xmax: ' + '\t' + str(shapeBox.xmax))
                        shp.write('\n' + 'Ymax: ' + '\t' + str(shapeBox.ymax))
                        n_points = unpack('<i', fp.read(4))
                        shp.write('\n' + 'Total Number of Points' + '\t' + str(n_points))
                        points = unpack('<' + ''.join(['dd'] * n_points), fp.read(n_points * 16))
                        shp.write('\n' + 'Coordinates of Points(X, Y): ')
                        for i in range(0, len(points)-1, 2):
                            shp.write('\n' + str(points[i]) + ', ' + str(points[i+1]))
                    except:
                        break
            if shape_type == 11: #PointZ
                while True:
                    try:
                        shp.write('\n')
                        record_number, content_length = unpack('>ii', fp.read(8))
                        shp.write('\n' + 'Record Number: ' + '\t' + str(record_number))
                        shp.write('\n' + 'Content Number: ' + '\t' + str(content_length))
                        shp.write('\n' + 'Shape Type: ' + '\t' + str(unpack('<i', fp.read(4))))
                        shp.write('\n' + 'X: ' + '\t' + str(unpack('<d', fp.read(8))))
                        shp.write('\n' + 'Y: ' + '\t' + str(unpack('<d', fp.read(8))))
                        shp.write('\n' + 'Z: ' + '\t' + str(unpack('<d', fp.read(8))))
                        shp.write('\n' + 'Measure: ' + '\t' + str(unpack('<d', fp.read(8))))
                    except:
                        break
            if shape_type == 13: #PolyLineZ
                while True:
                    try:
                        shp.write('\n')
                        record_number, content_length = unpack('>ii', fp.read(8))
                        shp.write('\n' + 'Record Number: ' + '\t' + str(record_number))
                        shp.write('\n' + 'Content Number: ' + '\t' + str(content_length))
                        shp.write('\n' + 'Shape Type: ' + '\t' + str(unpack('<i', fp.read(4))))
                        shapeBox = ShapeBox._make(unpack('<dddd', fp.read(32)))
                        shp.write('\n' + 'Xmin: ' + '\t' + str(shapeBox.xmin))
                        shp.write('\n' + 'Ymin: ' + '\t' + str(shapeBox.ymin))
                        shp.write('\n' + 'Xmax: ' + '\t' + str(shapeBox.xmax))
                        shp.write('\n' + 'Ymax: ' + '\t' + str(shapeBox.ymax))
                        numparts, numpoints = unpack('<ii', fp.read(8))
                        shp.write('\n' + 'Number of Parts: ' + str(numparts))
                        shp.write('\n' + 'Number of Points: ' + str(numpoints))
                        parts = unpack('<' + ''.join(['i'] * numparts), fp.read(numparts * 4))
                        shp.write('\n' + "Index List Part's First Points: " + str(parts))
                        points = unpack('<' + ''.join(['dd'] * numpoints), fp.read(numpoints * 16))
                        shp.write('\n' + 'Coordinates of Points(X, Y): ')
                        for i in range(0, len(points) - 1, 2):
                            shp.write('\n' + str(points[i]) + ', ' + str(points[i + 1]))
                        shp.write('\n' + 'Zmin: ' + '\t' + str(unpack('<d', fp.read(8))))
                        shp.write('\n' + 'Zmax: ' + '\t' + str(unpack('<d', fp.read(8))))
                        points_z = unpack('<' + ''.join(['d'] * numpoints), fp.read(numpoints * 8))
                        shp.write('\n' + 'Coordinates of Points(Z): ')
                        for i in range(0, len(points_z)):
                            shp.write('\n' + str(points_z[i]))
                        shp.write('\n' + 'Mmin: ' + str(unpack('<d', fp.read(8))))
                        shp.write('\n' + 'Mmax: ' + str(unpack('<d', fp.read(8))))
                        m_points = unpack('<' + ''.join(['d'] * numpoints), fp.read(numpoints * 8))
                        shp.write('\n' + "Measures of parts: ")
                        for i in range(0, len(m_points)):
                            shp.write('\n' + str(m_points[i]))
                    except:
                        break
            if shape_type == 15: #PolygonZ
                while True:
                    try:
                        shp.write('\n')
                        record_number, content_length = unpack('>ii', fp.read(8))
                        shp.write('\n' + 'Record Number: ' + '\t' + str(record_number))
                        shp.write('\n' + 'Content Number: ' + '\t' + str(content_length))
                        shp.write('\n' + 'Shape Type: ' + '\t' + str(unpack('<i', fp.read(4))))
                        shapeBox = ShapeBox._make(unpack('<dddd', fp.read(32)))
                        shp.write('\n' + 'Xmin: ' + '\t' + str(shapeBox.xmin))
                        shp.write('\n' + 'Ymin: ' + '\t' + str(shapeBox.ymin))
                        shp.write('\n' + 'Xmax: ' + '\t' + str(shapeBox.xmax))
                        shp.write('\n' + 'Ymax: ' + '\t' + str(shapeBox.ymax))
                        numparts, numpoints = unpack('<ii', fp.read(8))
                        shp.write('\n' + 'Number of Parts: ' + str(numparts))
                        shp.write('\n' + 'Number of Points: ' + str(numpoints))
                        parts = unpack('<' + ''.join(['i'] * numparts), fp.read(numparts * 4))
                        shp.write('\n' + "Index List Part's First Points: " + str(parts))
                        points = unpack('<' + ''.join(['dd'] * numpoints), fp.read(numpoints * 16))
                        shp.write('\n' + 'Coordinates of Points(X, Y): ')
                        for i in range(0, len(points) - 1, 2):
                            shp.write('\n' + str(points[i]) + ', ' + str(points[i + 1]))
                        shp.write('\n' + 'Zmin: ' + '\t' + str(unpack('<d', fp.read(8))))
                        shp.write('\n' + 'Zmax: ' + '\t' + str(unpack('<d', fp.read(8))))
                        points_z = unpack('<' + ''.join(['d'] * numpoints), fp.read(numpoints * 8))
                        shp.write('\n' + 'Coordinates of Points(Z): ')
                        for i in range(0, len(points_z)):
                            shp.write('\n' + str(points_z[i]))
                        shp.write('\n' + 'Mmin: ' + str(unpack('<d', fp.read(8))))
                        shp.write('\n' + 'Mmax: ' + str(unpack('<d', fp.read(8))))
                        m_points = unpack('<' + ''.join(['d'] * numpoints), fp.read(numpoints * 8))
                        shp.write('\n' + "Measures of parts: ")
                        for i in range(0, len(m_points)):
                            shp.write('\n' + str(m_points[i]))
                    except:
                        break
            if shape_type == 18: #MultiPointZ
                while True:
                    try:
                        shp.write('\n')
                        record_number, content_length = unpack('>ii', fp.read(8))
                        shp.write('\n' + 'Record Number: ' + '\t' + str(record_number))
                        shp.write('\n' + 'Content Number: ' + '\t' + str(content_length))
                        shp.write('\n' + 'Shape Type: ' + '\t' + str(unpack('<i', fp.read(4))))
                        shapeBox = ShapeBox._make(unpack('<dddd', fp.read(32)))
                        shp.write('\n' + 'Xmin: ' + '\t' + str(shapeBox.xmin))
                        shp.write('\n' + 'Ymin: ' + '\t' + str(shapeBox.ymin))
                        shp.write('\n' + 'Xmax: ' + '\t' + str(shapeBox.xmax))
                        shp.write('\n' + 'Ymax: ' + '\t' + str(shapeBox.ymax))
                        numpoints = unpack('<i', fp.read(4))
                        shp.write('\n' + 'Number of Points: ' + str(numpoints))
                        points = unpack('<' + ''.join(['dd'] * numpoints), fp.read(numpoints * 16))
                        shp.write('\n' + 'Coordinates of Points(X, Y): ')
                        for i in range(0, len(points) - 1, 2):
                            shp.write('\n' + str(points[i]) + ', ' + str(points[i + 1]))
                        shp.write('\n' + 'Zmin: ' + '\t' + str(unpack('<d', fp.read(8))))
                        shp.write('\n' + 'Zmax: ' + '\t' + str(unpack('<d', fp.read(8))))
                        points_z = unpack('<' + ''.join(['d'] * numpoints), fp.read(numpoints * 8))
                        shp.write('\n' + 'Coordinates of Points(Z): ')
                        for i in range(0, len(points_z)):
                            shp.write('\n' + str(points_z[i]))
                        shp.write('\n' + 'Mmin: ' + str(unpack('<d', fp.read(8))))
                        shp.write('\n' + 'Mmax: ' + str(unpack('<d', fp.read(8))))
                        m_points = unpack('<' + ''.join(['d'] * numpoints), fp.read(numpoints * 8))
                        shp.write('\n' + "Measures of parts: ")
                        for i in range(0, len(m_points)):
                            shp.write('\n' + str(m_points[i]))
                    except:
                        break
            if shape_type == 21: #PointM
                while True:
                    try:
                        shp.write('\n')
                        record_number, content_length = unpack('>ii', fp.read(8))
                        shp.write('\n' + 'Record Number: ' + '\t' + str(record_number))
                        shp.write('\n' + 'Content Number: ' + '\t' + str(content_length))
                        shp.write('\n' + 'Shape Type: ' + '\t' + str(unpack('<i', fp.read(4))))
                        shp.write('\n' + 'X: ' + '\t' + str(unpack('<d', fp.read(8))))
                        shp.write('\n' + 'Y: ' + '\t' + str(unpack('<d', fp.read(8))))
                        shp.write('\n' + 'M: ' + '\t' + str(unpack('<d', fp.read(8))))
                    except:
                        break
            if shape_type == 23: #PolyLineM
                while True:
                    try:
                        shp.write('\n')
                        record_number, content_length = unpack('>ii', fp.read(8))
                        shp.write('\n' + 'Record Number: ' + '\t' + str(record_number))
                        shp.write('\n' + 'Content Number: ' + '\t' + str(content_length))
                        shp.write('\n' + 'Shape Type: ' + '\t' + str(unpack('<i', fp.read(4))))
                        shapeBox = ShapeBox._make(unpack('<dddd', fp.read(32)))
                        shp.write('\n' + 'Xmin: ' + '\t' + str(shapeBox.xmin))
                        shp.write('\n' + 'Ymin: ' + '\t' + str(shapeBox.ymin))
                        shp.write('\n' + 'Xmax: ' + '\t' + str(shapeBox.xmax))
                        shp.write('\n' + 'Ymax: ' + '\t' + str(shapeBox.ymax))
                        numparts, numpoints = unpack('<ii', fp.read(8))
                        shp.write('\n' + 'Number of Parts: ' + str(numparts))
                        shp.write('\n' + 'Number of Points: ' + str(numpoints))
                        parts = unpack('<' + ''.join(['i'] * numparts), fp.read(numparts * 4))
                        shp.write('\n' + "Index List Part's First Points: " + str(parts))
                        points = unpack('<' + ''.join(['dd'] * numpoints), fp.read(numpoints * 16))
                        shp.write('\n' + 'Coordinates of Points(X, Y): ')
                        for i in range(0, len(points) - 1, 2):
                            shp.write('\n' + str(points[i]) + ', ' + str(points[i + 1]))
                        shp.write('\n' + 'Mmin: ' + str(unpack('<d', fp.read(8))))
                        shp.write('\n' + 'Mmax: ' + str(unpack('<d', fp.read(8))))
                        m_points = unpack('<' + ''.join(['d'] * numpoints), fp.read(numpoints * 8))
                        shp.write('\n' + "Measures of parts: ")
                        for i in range(0, len(m_points)):
                            shp.write('\n' + str(m_points[i]))
                    except:
                        break
            if shape_type == 25: #PolygonM
                while True:
                    try:
                        shp.write('\n')
                        record_number, content_length = unpack('>ii', fp.read(8))
                        shp.write('\n' + 'Record Number: ' + '\t' + str(record_number))
                        shp.write('\n' + 'Content Number: ' + '\t' + str(content_length))
                        shp.write('\n' + 'Shape Type: ' + '\t' + str(unpack('<i', fp.read(4))))
                        shapeBox = ShapeBox._make(unpack('<dddd', fp.read(32)))
                        shp.write('\n' + 'Xmin: ' + '\t' + str(shapeBox.xmin))
                        shp.write('\n' + 'Ymin: ' + '\t' + str(shapeBox.ymin))
                        shp.write('\n' + 'Xmax: ' + '\t' + str(shapeBox.xmax))
                        shp.write('\n' + 'Ymax: ' + '\t' + str(shapeBox.ymax))
                        numparts, numpoints = unpack('<ii', fp.read(8))
                        shp.write('\n' + 'Number of Parts: ' + str(numparts))
                        shp.write('\n' + 'Number of Points: ' + str(numpoints))
                        parts = unpack('<' + ''.join(['i'] * numparts), fp.read(numparts * 4))
                        shp.write('\n' + "Index List Part's First Points: " + str(parts))
                        points = unpack('<' + ''.join(['dd'] * numpoints), fp.read(numpoints * 16))
                        shp.write('\n' + 'Coordinates of Points(X, Y): ')
                        for i in range(0, len(points) - 1, 2):
                            shp.write('\n' + str(points[i]) + ', ' + str(points[i + 1]))
                        shp.write('\n' + 'Mmin: ' + str(unpack('<d', fp.read(8))))
                        shp.write('\n' + 'Mmax: ' + str(unpack('<d', fp.read(8))))
                        m_points = unpack('<' + ''.join(['d'] * numpoints), fp.read(numpoints * 8))
                        shp.write('\n' + "Measures of parts: ")
                        for i in range(0, len(m_points)):
                            shp.write('\n' + str(m_points[i]))
                    except:
                        break
            if shape_type == 28: #MultiPointM
                while True:
                    try:
                        shp.write('\n')
                        record_number, content_length = unpack('>ii', fp.read(8))
                        shp.write('\n' + 'Record Number: ' + '\t' + str(record_number))
                        shp.write('\n' + 'Content Number: ' + '\t' + str(content_length))
                        shp.write('\n' + 'Shape Type: ' + '\t' + str(unpack('<i', fp.read(4))))
                        shapeBox = ShapeBox._make(unpack('<dddd', fp.read(32)))
                        shp.write('\n' + 'Xmin: ' + '\t' + str(shapeBox.xmin))
                        shp.write('\n' + 'Ymin: ' + '\t' + str(shapeBox.ymin))
                        shp.write('\n' + 'Xmax: ' + '\t' + str(shapeBox.xmax))
                        shp.write('\n' + 'Ymax: ' + '\t' + str(shapeBox.ymax))
                        numpoints = unpack('<i', fp.read(4))[0]
                        shp.write('\n' + 'Number of Points: ' + str(numpoints))
                        points = unpack('<' + ''.join(['dd'] * numpoints), fp.read(numpoints * 16))
                        shp.write('\n' + 'Coordinates of Points(X, Y): ')
                        for i in range(0, len(points) - 1, 2):
                            shp.write('\n' + str(points[i]) + ', ' + str(points[i + 1]))
                        shp.write('\n' + 'Mmin: ' + str(unpack('<d', fp.read(8))))
                        shp.write('\n' + 'Mmax: ' + str(unpack('<d', fp.read(8))))
                        m_points = unpack('<' + ''.join(['d'] * numpoints), fp.read(numpoints * 8))
                        shp.write('\n' + "Measures of parts: ")
                        for i in range(0, len(m_points)):
                            shp.write('\n' + str(m_points[i]))
                    except:
                        break
            if shape_type == 31: #MultiPatch
                while True:
                    try:
                        shp.write('\n')
                        record_number, content_length = unpack('>ii', fp.read(8))
                        shp.write('\n' + 'Record Number: ' + '\t' + str(record_number))
                        shp.write('\n' + 'Content Number: ' + '\t' + str(content_length))
                        shp.write('\n' + 'Shape Type: ' + '\t' + str(unpack('<i', fp.read(4))))
                        shapeBox = ShapeBox._make(unpack('<dddd', fp.read(32)))
                        shp.write('\n' + 'Xmin: ' + '\t' + str(shapeBox.xmin))
                        shp.write('\n' + 'Ymin: ' + '\t' + str(shapeBox.ymin))
                        shp.write('\n' + 'Xmax: ' + '\t' + str(shapeBox.xmax))
                        shp.write('\n' + 'Ymax: ' + '\t' + str(shapeBox.ymax))
                        numparts, numpoints = unpack('<ii', fp.read(8))
                        shp.write('\n' + 'Number of Parts: ' + str(numparts))
                        shp.write('\n' + 'Number of Points: ' + str(numpoints))
                        parts = unpack('<' + ''.join(['i'] * numparts), fp.read(numparts * 4))
                        shp.write('\n' + "Index List Part's First Points: " + str(parts))
                        types = unpack('<' + ''.join(['i'] * numparts), fp.read(numparts * 4))
                        shp.write('\n' + 'Part Types List: ' + str(types))
                        points = unpack('<' + ''.join(['dd'] * numpoints), fp.read(numpoints * 16))
                        shp.write('\n' + 'Coordinates of Points(X, Y): ')
                        for i in range(0, len(points) - 1, 2):
                            shp.write('\n' + str(points[i]) + ', ' + str(points[i + 1]))
                        shp.write('\n' + 'Zmin' + str(unpack('<d', fp.read(8))))
                        shp.write('\n' + 'Zmax' + str(unpack('<d', fp.read(8))))
                        z_points = unpack('<' + ''.join(['d'] * numpoints), fp.read(numpoints * 8))
                        shp.write('\n' + 'Coordinates of Points(Z): ')
                        for i in range(0, len(z_points)):
                            shp.write('\n' + str(z_points[i]))
                        shp.write('\n' + 'Mmin: ' + str(unpack('<d', fp.read(8))))
                        shp.write('\n' + 'Mmax: ' + str(unpack('<d', fp.read(8))))
                        m_points = unpack('<' + '' .join(['d'] * numpoints), fp.read(numpoints * 8))
                        shp.write('\n' + "Measures of parts: ")
                        for i in range(0, len(m_points)):
                            shp.write('\n' + str(m_points[i]))
                    except:
                        break

def shx2txt(shx_path):
    # This function reads .shx file and prints all information to a .txt file.
    # Parameter: File name
    file_name = shx_path.split('.')[0]
    extension = '.txt'
    with open (shx_path, 'rb') as fp:
        with open(file_name + 'SHX' + extension, 'w') as shx:
            f_code, *_, f_length = unpack('>iiiiiii', fp.read(28))
            shx.write('File Code: ' + '\t' + str(f_code))
            shx.write('\n' + 'File Length: ' + '\t' + str(f_length))
            f_version, shape_type = unpack('<ii', fp.read(8))
            shx.write('\n' + 'Version :' + '\t' + str(f_version))
            shx.write('\n' + 'Shape Type: ' + '\t' + str(shape_type))
            boundingBox = BoundingBox._make(unpack('<dddddddd', fp.read(64)))
            shx.write('\n' + 'Xmin: ' + '\t' + str(boundingBox.xmin))
            shx.write('\n' + 'Ymin: ' + '\t' + str(boundingBox.ymin))
            shx.write('\n' + 'Xmax: ' + '\t' + str(boundingBox.xmax))
            shx.write('\n' + 'Ymax: ' + '\t' + str(boundingBox.ymax))
            shx.write('\n' + 'Zmin: ' + '\t' + str(boundingBox.zmin))
            shx.write('\n' + 'Zmax: ' + '\t' + str(boundingBox.zmax))
            shx.write('\n' + 'Mmin: ' + '\t' + str(boundingBox.mmin))
            shx.write('\n' + 'Mmax: ' + '\t' + str(boundingBox.mmax))
            while True:
                try:
                    shx.write('\n')
                    shx.write('\n' + 'Offset: ' + '\t' + str(unpack('>i', fp.read(4))[0]))
                    shx.write('\n' + 'Content Length: ' + '\t' + str(unpack('>i', fp.read(4))[0]))
                except:
                    break

def dbf2txt(dbf_path):
    # This function reads .dbf file and prints all information to a .txt file.
    # Parameter: File name
    file_name = dbf_path.split('.')[0]
    extension = '.txt'
    table = DBF(dbf_path, load = True)
    with open(file_name + 'DBF' + extension, 'w') as dbf:
        for key, value in table.records[0].items():
            dbf.write(key + '\t')
        dbf.write('\n')
        for i in range(len(table)):
            for key, value in table.records[i].items():
                dbf.write(str(value) + '\t')
            dbf.write('\n')

# Searching directory for files
file_exists = False
extension_shp = False
extension_shx = False
extension_dbf = False
FILE_EXTENSIONS = ('shp', 'dbf', 'shx')
while True:
    path = input("Please enter the file name without extension: ")
    for roots, directories, files in os.walk(os.getcwd()):
        for file in files:
            file_name = file.split(".")[0]
            file_extension = file.split(".")[1]
            if path == file_name:
                file_exists = True
                if file_extension in FILE_EXTENSIONS:
                    if file_extension == 'shp':
                        extension_shp = True
                        shp2txt(file)
                    if file_extension == 'shx':
                        extension_shx = True
                        shx2txt(file)
                    if file_extension == 'dbf':
                        extension_dbf = True
                        dbf2txt(file)
    if file_exists == False:
        print("This filename could not find in this directory. Try again.")
    elif (extension_shp  == False) or (extension_shx  == False) or (extension_dbf == False):
        print("A shapefile consists of a main file, an index file and a database table.\nIn this directory, this structure was not found to match the file name you entered. Please check.")
    else:
        break

