# Directory of Federal Real Property (DFRP) XML parser/exporter
# Tested with Python 2.7.10
# Created by Randal Greene (rgreene@feaverslane.com), February 2018

# Input: XML dump of real property, described at https://www.tbs-sct.gc.ca/dfrp-rbif/home-accueil-eng.aspx and
#        downloaded from https://www.tbs-sct.gc.ca/dfrp-rbif/opendata-eng.aspx
# Output: CSV tables that can be imported into a relational database system or GIS software
# Note: Exports UTF-8 encoding; non-ASCII characters will display incorrectly in Excel, which assumes UTF-16
#       To output French text, search and replace '_E' with '_F'; you may also want to translate field names
#       You may wish to force Property_Number, Parcel_number, Structure_Number, FederalSiteIdentifier to a string when
#       importing:
#           In Excel, do this by customizing the CSV import specification
#           In ArcGIS, use a schema.ini file

# License: CC-BY-SA (see https://creativecommons.org/licenses/by-sa/4.0/legalcode)


import xml.etree.ElementTree as ET
import unicodecsv as csv


# replace with appropriate local path
starting_path = 'C:/GIS/DFRP/'


# function to check for optional element, with optional sub-element and sub-sub-element, and return element text
# check for both the "doesn't exist" case and the "empty element" case (although it appears the data only has latter)
def optional_element_lookup(parent_element, element_name, sub_element_name=None, sub_sub_element_name=None):
    ret = ''
    element = parent_element.find(element_name)
    if element is not None:
        if sub_element_name is not None:
            sub_element = element.find(sub_element_name)
            if sub_element is not None:
                if sub_sub_element_name is not None:
                    sub_sub_element = sub_element.find(sub_sub_element_name)
                    if sub_sub_element is not None:
                        if sub_sub_element.text is not None:
                            ret = sub_sub_element.text
                else:
                    if sub_element.text is not None:
                        ret = sub_element.text
        else:
            if element.text is not None:
                ret = element.text
    return ret


# function to check for optional attribute, and return element text
def optional_attribute_lookup(element, attribute):
    ret = element.get(attribute)
    if ret is None:
        ret = ''
    return ret


# function to check whether the passed custodian has already been added to the custodian lookup table, and if not add it
def check_add_custodian(parent_element, custodian_codes, custodian_writer):
    custodian = parent_element.find('Custodian')
    code = custodian.get('code')
    if code not in custodian_codes:
        custodian_codes.append(code)
        # optional attributes
        isDepartment = optional_attribute_lookup(custodian, 'isDepartment')
        isAgency = optional_attribute_lookup(custodian, 'isAgency')
        isCrownCorporation = optional_attribute_lookup(custodian, 'isCrownCorporation')
        portfolioLastCertifiedDate = optional_attribute_lookup(custodian, 'portfolioLastCertifiedDate')
        # optional elements
        Official_Contact_Name = optional_element_lookup(custodian, 'Official_Contact_Name')
        Official_Contact_Telephone = optional_element_lookup(custodian, 'Official_Contact_Telephone')
        Official_Contact_Email = optional_element_lookup(custodian, 'Official_Contact_Email')
        Official_Contact_Webform = optional_element_lookup(custodian, 'Official_Contact_Webform')
        # output
        custodian_writer.writerow([code,
                                   isDepartment,
                                   isAgency,
                                   isCrownCorporation,
                                   portfolioLastCertifiedDate,
                                   custodian.find('Name_E').text,
                                   Official_Contact_Name,
                                   Official_Contact_Telephone,
                                   Official_Contact_Email,
                                   Official_Contact_Webform])
    return code


# main logic
root = ET.parse(starting_path + 'dfrp-rbif.xml').getroot()

# Properties
try:
    # build lookup table of unique custodian values
    custodian_codes = []
    custodian_file = open(starting_path + 'custodian.csv', 'wb')
    custodian_writer = csv.writer(custodian_file, dialect='excel', encoding='utf-8')
    # main table
    property_file = open(starting_path + 'property.csv', 'wb')
    property_writer = csv.writer(property_file, dialect='excel', encoding='utf-8')
    # 1:M related tables
    parcel_file = open(starting_path + 'parcel.csv', 'wb')
    parcel_writer = csv.writer(parcel_file, dialect='excel', encoding='utf-8')
    structure_file = open(starting_path + 'structure.csv', 'wb')
    structure_writer = csv.writer(structure_file, dialect='excel', encoding='utf-8')
    structure_photo_file = open(starting_path + 'structure_photo.csv', 'wb')
    structure_photo_writer = csv.writer(structure_photo_file, dialect='excel', encoding='utf-8')
    tenant_file = open(starting_path + 'tenant.csv', 'wb')
    tenant_writer = csv.writer(tenant_file, dialect='excel', encoding='utf-8')
    federal_contaminated_site_file = open(starting_path + 'federal_contaminated_site.csv', 'wb')
    federal_contaminated_site_writer = csv.writer(federal_contaminated_site_file, dialect='excel', encoding='utf-8')
    property_photo_file = open(starting_path + 'property_photo.csv', 'wb')
    property_photo_writer = csv.writer(property_photo_file, dialect='excel', encoding='utf-8')

    # column headers
    custodian_writer.writerow(['code',
                               'isDepartment',
                               'isAgency',
                               'isCrownCorporation',
                               'portfolioLastCertifiedDate',
                               'Name',
                               'Official_Contact_Name',
                               'Official_Contact_Telephone',
                               'Official_Contact_Email',
                               'Official_Contact_WebForm'])
    property_writer.writerow(['lastModifiedDate',
                              'createdDate',
                              'Property_Number',
                              'Custodian_code',
                              'Property_Name',
                              'Address',
                              'Primary_Use',
                              'Interest_Type',
                              'Restriction_on_Interest',
                              'MiniMap'])
    parcel_writer.writerow(['Property_Number',
                            'Parcel_number',
                            'Land_Area',
                            'Land_Area_unitofMeasure',
                            'Building_Count',
                            'Floor_Area',
                            'Floor_Area_unitofMeasure',
                            'ExteriorParkingSpaces',
                            'InteriorParkingSpaces',
                            'InteriorParkingSpaces_includedInFloorArea',
                            'Location_type',
                            'Location_sgc',
                            'Location_fed',
                            'Location_inUrbanArea',
                            'Location_inRuralArea',
                            'Location_inIsolatedArea',
                            'Location_Province',
                            'Location_Metro_Area_Name',
                            'Location_Municipality',
                            'Location_Place_Name',
                            'Location_Federal_Electoral_District',
                            'Location_Latitude',
                            'Location_Longitude',
                            'Location_PositionalAccuracy',
                            'Location_PositionalAccuracy_unitofMeasure',
                            'Location_Country_Name',
                            'Location_City_Name'])
    structure_writer.writerow(['Property_Number',
                               'Parcel_number',
                               'Structure_Number',
                               'occupancy',
                               'createdDate',
                               'lastModifiedDate',
                               'Custodian_code',
                               'Structure_Name',
                               'Address',
                               'Latitude',
                               'Longitude',
                               'Interest_Type',
                               'Condition',
                               'Floor_Area',
                               'Floor_Area_unitofMeasure',
                               'MiniMap',
                               'UseTypes'])
    structure_photo_writer.writerow(['Property_Number',
                                     'Parcel_number',
                                     'Structure_Number',
                                     'Photo'])
    tenant_writer.writerow(['Property_Number',
                            'Parcel_number',
                            'Structure_Number',
                            'code',
                            'Name',
                            'Floor_Area',
                            'Floor_Area_unitofMeasure'])
    federal_contaminated_site_writer.writerow(['Property_Number',
                                               'FederalSiteID'])
    property_photo_writer.writerow(['Property_Number',
                                    'Photo'])

    # data rows
    for Property in root.findall('Property'):
        # lookup table of unique custodian values
        code = check_add_custodian(Property, custodian_codes, custodian_writer)

        # Properties - main table
        # optional elements
        Property_Name = optional_element_lookup(Property, 'Property_Name_E')
        Address = optional_element_lookup(Property, 'Address_E')
        MiniMap = optional_element_lookup(Property, 'MiniMap')
        # output
        property_writer.writerow([Property.get('lastModifiedDate'),
                                  Property.get('createdDate'),
                                  Property.find('Property_Number').text,
                                  code,
                                  Property_Name,
                                  Address,
                                  Property.find('Primary_Use_E').text,
                                  Property.find('Interest_Type_E').text,
                                  Property.find('Restriction_on_Interest_E').text,
                                  MiniMap])

        # 1:m related tables
        # Parcels
        Parcels = Property.find("Parcels")
        if Parcels is not None:
            for Parcel in Parcels.findall("Parcel"):
                # optional attributes and elements
                Location = Parcel.find('Location')
                Location_sgc = optional_attribute_lookup(Location, 'sgc')
                Location_fed = optional_attribute_lookup(Location, 'fed')
                Location_inUrbanArea = optional_attribute_lookup(Location, 'inUrbanArea')
                Location_inRuralArea = optional_attribute_lookup(Location, 'inRuralArea')
                Location_inIsolatedArea = optional_attribute_lookup(Location, 'inIsolatedArea')
                ExteriorParkingSpaces = optional_element_lookup(Parcel, 'ParkingSpaces', 'Exterior')
                InteriorParkingSpaces = optional_element_lookup(Parcel, 'ParkingSpaces', 'Interior')
                InteriorParkingSpaces_includedInFloorArea = ''
                if len(InteriorParkingSpaces) > 0:
                    InteriorParkingSpaces_includedInFloorArea = Parcel.find('ParkingSpaces').find('Interior').get(
                        'includedInFloorArea')
                Location_Province = optional_element_lookup(Location, 'Province_E')
                Location_Metro_Area_Name = optional_element_lookup(Location, 'Metro_Area_Name_E')
                Location_Municipality = optional_element_lookup(Location, 'Municipality_E')
                Location_Place_Name = optional_element_lookup(Location, 'Place_Name')
                Location_Federal_Electoral_District = optional_element_lookup(Location, 'Federal_Electoral_District_E')
                Location_Latitude = optional_element_lookup(Location, 'Latitude')
                Location_Longitude = optional_element_lookup(Location, 'Longitude')
                Positional_Accuracy = Location.find('Positional_Accuracy')
                Location_Positional_Accuracy = optional_element_lookup(Location, 'Positional_Accuracy')
                Location_Positional_Accuracy_unitofMeasure = ''
                if Positional_Accuracy is not None:
                    Location_Positional_Accuracy_unitofMeasure = optional_attribute_lookup(Positional_Accuracy,
                                                                                           'unitofMeasure')
                Location_Country_Name = optional_element_lookup(Location, 'Country_Name_E')
                Location_City_Name = optional_element_lookup(Location, 'City_Name_E')

                # output
                parcel_writer.writerow([Property.find('Property_Number').text,
                                        Parcel.get('number'),
                                        Parcel.find('Land_Area').text,
                                        Parcel.find('Land_Area').get('unitofMeasure'),
                                        Parcel.find('Building_Count').text,
                                        Parcel.find('Floor_Area').text,
                                        Parcel.find('Land_Area').get('unitofMeasure'),
                                        ExteriorParkingSpaces,
                                        InteriorParkingSpaces,
                                        InteriorParkingSpaces_includedInFloorArea,
                                        Location.get('type'),
                                        Location_sgc,
                                        Location_fed,
                                        Location_inUrbanArea,
                                        Location_inRuralArea,
                                        Location_inIsolatedArea,
                                        Location_Province,
                                        Location_Metro_Area_Name,
                                        Location_Municipality,
                                        Location_Place_Name,
                                        Location_Federal_Electoral_District,
                                        Location_Latitude,
                                        Location_Longitude,
                                        Location_Positional_Accuracy,
                                        Location_Positional_Accuracy_unitofMeasure,
                                        Location_Country_Name,
                                        Location_City_Name])

                # Structures
                Structures = Parcel.find("Structures")
                if Structures is not None:
                    for Structure in Structures.findall("Structure"):
                        # lookup table of unique custodian values
                        code = check_add_custodian(Structure, custodian_codes, custodian_writer)

                        # optional elements
                        Address = optional_element_lookup(Structure, 'Address_E')
                        Latitude = optional_element_lookup(Structure, 'Location', 'Latitude')
                        Longitude = optional_element_lookup(Structure, 'Location', 'Longitude')
                        Condition = optional_element_lookup(Structure, 'Condition_E')
                        MiniMap = optional_element_lookup(Structure, 'MiniMap')
                        # 1:M elements
                        UseTypesText = ''
                        UseTypes = Structure.find('UseTypes')
                        for UseType in UseTypes:
                            if len(UseTypesText) > 0:
                                UseTypesText += ' | '
                            UseTypesText += UseType.find('Use_Name_E').text
                        # output
                        structure_writer.writerow([Property.find('Property_Number').text,
                                                   Parcel.get('number'),
                                                   Structure.find('Structure_Number').text,
                                                   Structure.get('occupancy'),
                                                   Structure.get('createdDate'),
                                                   Structure.get('lastModifiedDate'),
                                                   code,
                                                   Structure.find('Structure_Name_E').text,
                                                   Address,
                                                   Latitude,
                                                   Longitude,
                                                   Structure.find('Interest_Type_E').text,
                                                   Condition,
                                                   Structure.find('Floor_Area').text,
                                                   Structure.find('Floor_Area').get('unitofMeasure'),
                                                   MiniMap,
                                                   UseTypesText])

                        # Tenants
                        Tenants = Structure.find('Tenants')
                        if Tenants is not None:
                            # standard for loop not working here for some reason!!!
                            # for Tenant in Tenants.find('Tenant'):
                            for index in range(0, len(Tenants)):
                                Tenant = Tenants[index]
                                # output
                                tenant_writer.writerow([Property.find('Property_Number').text,
                                                        Parcel.get('number'),
                                                        Structure.find('Structure_Number').text,
                                                        Tenant.get('code'),
                                                        Tenant.find('Name_E').text,
                                                        Tenant.find('Floor_Area').text,
                                                        Tenant.find('Floor_Area').get('unitofMeasure')])

                        # Structure Photos
                        Photos = Structure.find('Photos')
                        if Photos is not None:
                            for Photo in Photos:
                                structure_photo_writer.writerow([Property.find('Property_Number').text,
                                                                 Parcel.get('number'),
                                                                 Structure.find('Structure_Number').text,
                                                                 Photo.text])

        # Federal Contaminated Sites
        FederalContaminatedSites = Property.find('FederalContaminatedSites')
        if FederalContaminatedSites is not None:
            Sites = FederalContaminatedSites.findall('Site')
            for FederalContaminatedSite in Sites:
                # output
                federal_contaminated_site_writer.writerow([Property.find('Property_Number').text,
                                                           FederalContaminatedSite.get('FederalSiteIdentifier')])

        # Property Photos
        Photos = Property.find('Photos')
        if Photos is not None:
            for Photo in Photos:
                # output
                property_photo_writer.writerow([Property.find('Property_Number').text,
                                                Photo.text])

finally:
    if property_file is not None:
        property_file.close()
    if parcel_file is not None:
        parcel_file.close()
    if structure_file is not None:
        structure_file.close()
    if structure_photo_file is not None:
        structure_photo_file.close()
    if tenant_file is not None:
        tenant_file.close()
    if federal_contaminated_site_file is not None:
        federal_contaminated_site_file.close()
    if property_photo_file is not None:
        property_photo_file.close()
