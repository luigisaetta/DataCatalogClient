import oci
import hashlib
from ads.dataset.factory import DatasetFactory
import os
# utils to read from Data Catalog

#CATALOG_ID = "ocid1.datacatalog.oc1.eu-frankfurt-1.aaaaaaaap6lel4hqckltn7fvjnux42jepzohdktkceywlyrnnrwgolbupzhq"
# use the default namespace
#NAMESPACE_ID = "0e4d60d9-d5b5-467f-89bb-22db63a3ee18"
# to identify OS BUCKET in Catalog
#ASSETT_KEY = "6adf4ea3-67d5-44a3-b4f7-19fbf303d539"

class  ODSDataCatalog:
    def __init__(self,catalog_id,asset_key,namespace_id,bucket_name):
        self.catalog_id = catalog_id
        self.asset_key = asset_key
        self.namespace_id = namespace_id
        self.bucket_name = bucket_name
    
    def get_key_from_name(self,name):
        # for now it is hard coded, for the demo
        rps = oci.auth.signers.get_resource_principals_signer()
    
        dcat_client = oci.data_catalog.DataCatalogClient({}, signer=rps)
    
        search = dcat_client.list_entities(catalog_id=self.catalog_id,data_asset_key=self.asset_key).data
        for elem in search.items:
            if str(elem.display_name) == name:
                key_name = elem.key
        return key_name
    
    def get_hash_from_catalog(self,name):
        # get the signer
        rps = oci.auth.signers.get_resource_principals_signer()
    
        dcat_client = oci.data_catalog.DataCatalogClient({}, signer=rps)
    
        response = dcat_client.get_entity(catalog_id=self.catalog_id, 
                                  data_asset_key=self.asset_key, 
                                  entity_key=self.get_key_from_name(name))
        # md5 read from Catalog
        md5_cat = response.data.custom_property_members[-1].value
    
        return md5_cat

    def get_hash_from_file(self,FILE_NAME):
        # input is data store from ADS
        # get dataset from object storage, check MD5 hash
        BUCKET_NAME = self.bucket_name
        TMP_FILE = 'temp.csv'

        ds = DatasetFactory.open(f"ocis://{BUCKET_NAME}/{FILE_NAME}")

        print('The dataset contains:', ds.shape[0], 'records')

        # dump to a tmp file
        ds.to_csv('temp.csv', index=None)

        md5_computed = hashlib.md5(open(TMP_FILE,'rb').read()).hexdigest()

        os.remove(TMP_FILE)
        return md5_computed
                   
    