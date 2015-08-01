import os
import ee

EE_URL = 'https://earthengine.googleapis.com'
EE_ACCOUNT = '1047393292754-soobrfmc009mcqn9ca344fehnl5i2gie@developer.gserviceaccount.com'
EE_PRIVATE_KEY_FILE = 'privatekey.pem'


EE_CREDENTIALS = ee.ServiceAccountCredentials(
    EE_ACCOUNT, EE_PRIVATE_KEY_FILE
)

ee.Initialize(EE_CREDENTIALS, EE_URL)
ee.data.setDeadline(60000)
