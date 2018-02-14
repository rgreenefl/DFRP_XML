# DFRP_XML
Canadian Directory of Federal Real Property (DFRP) XML parser/exporter

Tested with Python 2.7.10

Created by Randal Greene (rgreene@feaverslane.com), February 2018

Input: XML dump of real property, described at https://www.tbs-sct.gc.ca/dfrp-rbif/home-accueil-eng.aspx and downloaded from https://www.tbs-sct.gc.ca/dfrp-rbif/opendata-eng.aspx

Output: CSV tables that can be imported into a relational database system or GIS software

Note:
* Exports UTF-8 encoding; non-ASCII characters will display incorrectly in Excel, which assumes UTF-16
* To output French text, search and replace '_E' with '_F'; you may also want to translate field names
* You may wish to force Property_Number, Parcel_number, Structure_Number, FederalSiteIdentifier to a string when importing:
    - In Excel, do this by customizing the CSV import specification
    - In ArcGIS, use a schema.ini file

License: CC-BY-SA (see https://creativecommons.org/licenses/by-sa/4.0/legalcode)
