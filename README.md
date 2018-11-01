# Labkey API Wrapper

**This package is a wrapper script which makes calls to Labkey's api. Labkey maintains their api. The offical Labkey API package can be accessed at https://github.com/LabKey/labkey-api-python**

Three simple steps to use Labkey’s API to get data from a Labkey project into a json file.
1. Install labkey 
2. Run the setup_netrc_file.py script to create netrc file.
3. Run the get_datasets.py script

### 1. To install labkey, simply use pip on the command line: 
	$ pip install labkey

Note: For users who installed this package before it was published to PyPI (before v0.3.0) it is recommended you uninstall and reinstall the package rather than attempting to upgrade. This is due to a change in the package's versioning semantics.

### 2. Run the setup_netrc_file.py script

There are two options to pass the UHN labkey login credentials:
#### 1. The user's email address and password: 
```
$ python setup_netrc_file.py -u user_email -p user_password
```
#### 2. An apikey (make sure to use quotes around the apikey to prevent an error): 
```
$ python setup_netrc_file.py -u apikey -p "apikey|c2616e2076f23b1dcf4b865f3c7d2i9h” 
```

Your login credentials will be stored in the .netrc file (_netrc file on windows) in your home directory. We recommend you use the apikey option in order to keep your username and password private. To use the apikey option, here is a well documented page from the offical Labkey website setup: https://www.labkey.org/Documentation/wiki-page.view?name=apikey

### 3. Run the get_datasets.py script 

Run the python script and pass the project_name, output file as additional arguments: 
```
$ python get_datasets.py -i “project_name” -o "output_file.json"
```

If you need further assistance using our API please contact us at labkey@uhnresearch.ca.
