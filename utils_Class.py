import oci
import hashlib
from ads.dataset.factory import DatasetFactory
import os


# utils to read from Data Catalog


class  ODSDataCatalog:
    def __init__(self, catalog_id, namespace_id, asset_key):
        # catalog id
        self.catalog_id = catalog_id
        
        # normally it is the default namespace in the DataCatalog
        # unless a custom namespace in dataCatalog has been defined and used
        # "0e4d60d9-d5b5-467f-89bb-22db63a3ee18"
        self.namespace_id = namespace_id # namespace
        
        # assett key, in this case the assett is the bucket
        self.asset_key = asset_key 
    
    #
    # print the list of Data Entities names (only the names)for the Data Assett
    # for more info see next function
    def print_entity_name_list(self):
        rps = oci.auth.signers.get_resource_principals_signer()
    
        dcat_client = oci.data_catalog.DataCatalogClient({}, signer=rps)
    
        list_entities = dcat_client.list_entities(catalog_id=self.catalog_id, data_asset_key=self.asset_key).data
        
        entity_name_list = []
        
        for elem in list_entities.items:
            entity_name_list.append(elem.display_name)
    
        entity_name_list = sorted(entity_name_list)
        
        print("The list of entities is:")
        print()
        
        for name in entity_name_list:
            print(name)
            
        return
    #
    # show all metadata associated with the Data Entity (file in a bucket)
    #
    def print_entity_list_raw(self):
        rps = oci.auth.signers.get_resource_principals_signer()
    
        dcat_client = oci.data_catalog.DataCatalogClient({}, signer=rps)
    
        list_entities = dcat_client.list_entities(catalog_id=self.catalog_id, data_asset_key=self.asset_key).data
        
        for elem in list_entities.items:
            print(elem.display_name)
            print("-------")
            print(elem)
        
    def get_key_from_name(self, name):
        rps = oci.auth.signers.get_resource_principals_signer()
    
        dcat_client = oci.data_catalog.DataCatalogClient({}, signer=rps)
    
        search = dcat_client.list_entities(catalog_id=self.catalog_id, data_asset_key=self.asset_key).data
        
        key_name = ''
        for elem in search.items:
            if str(elem.display_name) == name:
                key_name = elem.key # retrieve entity(file) access key
                
                # exit from loop
                break
        
        return key_name
    
    #
    # To get the custom property owner
    #
    def get_owner(self, name):
        # get the signer
        rps = oci.auth.signers.get_resource_principals_signer()
    
        dcat_client = oci.data_catalog.DataCatalogClient({}, signer=rps)
    
        response = dcat_client.get_entity(catalog_id=self.catalog_id, 
                                  data_asset_key=self.asset_key, 
                                  entity_key=self.get_key_from_name(name))
        # md5 read from Catalog
        search = response.data.custom_property_members
        
        for elem in search:
            
            if elem.display_name == 'owner':
                if elem.value == None:
                    print('No value registered in the data catalog!')
                    return '-'
                else:
                    owner = elem.value
                
                # exit from loop
                break
                
        return owner
    
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
<<<<<<< HEAD
                    print('No value registered in the data catalog!')
=======
                    print(BOLD+'No value registered in the data catalog!'+END)
>>>>>>> d92df674e88d904141821775c439b8cecfd5c4ed
                    return '-'
                else:
                    md5_cat = elem.value
                
                # exit from loop
                break
                
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
                    return '-'
                else:
                    md5_cat = elem.value
    
        return md5_cat

    def get_hash_from_file(self, name, bucket_name):
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
                   
