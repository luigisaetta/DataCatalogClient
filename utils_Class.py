import oci
import hashlib
from ads.dataset.factory import DatasetFactory
import os

# utils to read from Data Catalog

# for print formatting
BOLD = '\033[1m'
END = '\033[0m'

class  ODSDataCatalog:
    def __init__(self, catalog_id, asset_key, namespace_id):
        self.catalog_id = catalog_id # catalog id
	# assett key, in this case the assett is the bucket
        self.asset_key = asset_key 
	# normally it is the default namespace in the DataCatalog
        self.namespace_id = namespace_id # namespace
    
    def get_key_from_name(self, name):
        rps = oci.auth.signers.get_resource_principals_signer()
    
        dcat_client = oci.data_catalog.DataCatalogClient({}, signer=rps)
    
        search = dcat_client.list_entities(catalog_id=self.catalog_id, data_asset_key=self.asset_key).data
        key_name = ''
        for elem in search.items:
            if str(elem.display_name) == name:
                key_name = elem.key # retrieve entity(file) access key
        return key_name
    
    def get_hash_from_catalog(self, name):
        # get the signer
        rps = oci.auth.signers.get_resource_principals_signer()
    
        dcat_client = oci.data_catalog.DataCatalogClient({}, signer=rps)
    
        response = dcat_client.get_entity(catalog_id=self.catalog_id, 
                                  data_asset_key=self.asset_key, 
                                  entity_key=self.get_key_from_name(name))
        # md5 read from Catalog
        search = response.data.custom_property_members
        for elem in search:
            if elem.display_name == 'file_hash':
                if elem.value == None:
                    print(BOLD+'No value registered in the data catalog!'+END)
                    return None
                else:
                    md5_cat = elem.value
    
        return md5_cat
    
    def get_version_from_catalog(self, name):
        # get the signer
        rps = oci.auth.signers.get_resource_principals_signer()
    
        dcat_client = oci.data_catalog.DataCatalogClient({}, signer=rps)
    
        response = dcat_client.get_entity(catalog_id=self.catalog_id, 
                                  data_asset_key=self.asset_key, 
                                  entity_key=self.get_key_from_name(name))
        # version number read from Catalog
        search = response.data.custom_property_members
        for elem in search:
            if elem.display_name == 'file_version':
                if elem.value == None:
                    print(BOLD+'No value registered in the data catalog!'+END)
                    return None
                else:
                    md5_cat = elem.value
    
        return md5_cat

    def get_hash_from_file(self,name,bucket_name):
        # input is data store from ADS
        # get dataset from object storage, check MD5 hash
        TMP_FILE = 'temp.csv'
        try:
            ds = DatasetFactory.open(f"ocis://{bucket_name}/{name}")
            #break
        except FileNotFoundError as error:
            if str(error) == 'path %s/%s must be a file, a directory, or a bucket.' %(bucket_name,name):
                print(BOLD+'There is no such file in this OS bucket'+END)
            else:
                print(BOLD+'There is no such OS bucket'+END)
            return ''

        print('The dataset contains:', ds.shape[0], 'records')

        # dump to a tmp file
        ds.to_csv('temp.csv', index=None)

        md5_computed = hashlib.md5(open(TMP_FILE,'rb').read()).hexdigest()

        os.remove(TMP_FILE)
        return md5_computed
                   
    
