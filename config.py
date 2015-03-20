import os
import ee
from oauth2client.appengine import AppAssertionCredentials

EE_URL = 'https://earthengine.googleapis.com'
EE_ACCOUNT = '1047393292754-soobrfmc009mcqn9ca344fehnl5i2gie@developer.gserviceaccount.com'
EE_PRIVATE_KEY_FILE = 'privatekey.pem'


DEBUG_MODE = (
    'SERVER_SOFTWARE' in os.environ
    and os.environ['SERVER_SOFTWARE'].startswith('Dev')
)

if DEBUG_MODE:
    EE_CREDENTIALS = ee.ServiceAccountCredentials(
        EE_ACCOUNT, EE_PRIVATE_KEY_FILE
    )
else:
    EE_CREDENTIALS = AppAssertionCredentials(ee.OAUTH2_SCOPE)

ee.Initialize(EE_CREDENTIALS, EE_URL)
ee.data.setDeadline(60000)
