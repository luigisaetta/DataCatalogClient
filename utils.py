import oci
import hashlib

# utils to read from Data Catalog

CATALOG_ID = "ocid1.datacatalog.oc1.eu-frankfurt-1.aaaaaaaap6lel4hqckltn7fvjnux42jepzohdktkceywlyrnnrwgolbupzhq"
# use the default namespace
NAMESPACE_ID = "0e4d60d9-d5b5-467f-89bb-22db63a3ee18"
# to identify OS BUCKET in Catalog
ASSETT_KEY = "6adf4ea3-67d5-44a3-b4f7-19fbf303d539"

def get_hash_from_catalog(name):
    # get the signer
    rps = oci.auth.signers.get_resource_principals_signer()
    
    dcat_client = oci.data_catalog.DataCatalogClient({}, signer=rps)
    
    response = dcat_client.get_entity(catalog_id=CATALOG_ID, 
                                  data_asset_key=ASSETT_KEY, 
                                  entity_key=get_key_from_name(name))
    # md5 read from Catalog
    md5_cat = response.data.custom_property_members[1].value
    
    return md5_cat

def get_hash_from_file(dds):
    # input is data store from ADS
    return ""
                   
def get_key_from_name(name):
    # for now it is hard coded, for the demo
    
    return "680cdc2c-febb-45a7-b0f0-39301a296564"