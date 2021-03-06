import csv
import xml.dom.minidom
import sys

def convertDegreesMinSecToDecimal(coordinate):
  # takes a "degrees-minutes-seconds" format and converts to decimal
  # assumes the use of a "-" as the delimiter
  # todo: allow the use of whitespace delimiter or delimiter passed to function
  # formula for conversion is Degrees+(minutes/60)+(seconds/3600)
  
  # is the coordinate negative?
  #print "Coordinate = " + coordinate
  negative = 0
  if coordinate[0] == "-":
    negative = 1
    coordinate = coordinate.lstrip('-')
 
  # split apart the degrees, minutes, seconds into a list
  listOfDegreesMinutesSeconds = coordinate.split('-')
  # get degrees
  convertedCoordinate = float(listOfDegreesMinutesSeconds[0])
  # get minutes
  convertedCoordinate = convertedCoordinate + (float(listOfDegreesMinutesSeconds[1])/60)
  # get seconds 
  convertedCoordinate = convertedCoordinate + (float(listOfDegreesMinutesSeconds[2])/3600)
  
  if negative:
    convertedCoordinate = convertedCoordinate * -1
  #print "converted Coordinate is " + str(convertedCoordinate)
  return convertedCoordinate

def createPlacemark(kmlDoc, row, order):
  # This creates a  element for a row of data.
  # A row is a dict.
  placemarkElement = kmlDoc.createElement('Placemark')
  extElement = kmlDoc.createElement('ExtendedData')
  placemarkElement.appendChild(extElement)
  
  # Loop through the columns and create a  element for every field that has a value.
  for key in order:
    if row[key]:
      dataElement = kmlDoc.createElement('Data')
      dataElement.setAttribute('name', key)
      valueElement = kmlDoc.createElement('value')
      dataElement.appendChild(valueElement)
      valueText = kmlDoc.createTextNode(row[key])
      valueElement.appendChild(valueText)
      extElement.appendChild(dataElement)
  
  # Create a name attribute so the placemark displays correctly in Google Earth
  nameElement = kmlDoc.createElement('name')
  nameElement.appendChild(kmlDoc.createTextNode(row['Name']))
  placemarkElement.appendChild(nameElement)
  
  # Create the Point Element, convert the degrees-minutes-seconds format to 
  # decimal format, need to add test to see if conversion is needed
  pointElement = kmlDoc.createElement('Point')
  placemarkElement.appendChild(pointElement)
  latitude = convertDegreesMinSecToDecimal(row['Lat'])
  longitude = convertDegreesMinSecToDecimal(row['Long'])
  coordinates = str(longitude) + ',' + str(latitude)
  coorElement = kmlDoc.createElement('coordinates')
  coorElement.appendChild(kmlDoc.createTextNode(coordinates))
  pointElement.appendChild(coorElement)
  return placemarkElement

def createKML(csvReader, fileName, order):
  # This constructs the KML document from the CSV file.
  kmlDoc = xml.dom.minidom.Document()
  
  kmlElement = kmlDoc.createElementNS('http://earth.google.com/kml/2.2', 'kml')
  kmlElement.setAttribute('xmlns','http://earth.google.com/kml/2.2')
  kmlElement = kmlDoc.appendChild(kmlElement)
  documentElement = kmlDoc.createElement('Document')
  documentElement = kmlElement.appendChild(documentElement)

  # Skip the header line.
  csvReader.next()
  
  for row in csvReader:
    placemarkElement = createPlacemark(kmlDoc, row, order)
    documentElement.appendChild(placemarkElement)
  kmlFile = open(fileName, 'w')
  kmlFile.write(kmlDoc.toprettyxml('  ', newl = '\n', encoding = 'utf-8'))

def main():
  # This reader opens up 'sites.csv', 
  # It creates a KML file called 'sites.kml'.
  
  # If an argument was passed to the script, it splits the argument on a comma
  # and uses the resulting list to specify an order for when columns get added.
  # Otherwise, it defaults to the pre-defined order
  
  if len(sys.argv) >1: order = sys.argv[1].split(',')
  else: order = ['Name','LEC','Number_of_DS1s','City','State','County','Lat','Long','NPA-NXX','Zip','Technology', 'MSC_Location']
  csvreader = csv.DictReader(open('sites.csv'),order)
  kml = createKML(csvreader, 'sites.kml', order)
if __name__ == '__main__':
  main()