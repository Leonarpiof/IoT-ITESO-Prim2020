const char SECRET_ROOT_CERT[] PROGMEM =
"-----BEGIN CERTIFICATE-----"
"CA certificate here (Given by AWS publicly)"
"Certificate usally under the termination file.pem"
"The certificate may take many more code lines than this one"
"-----END CERTIFICATE-----";

const char SECRET_CLIENT_CERT[] PROGMEM =
"-----BEGIN CERTIFICATE-----"
"CA certificate here (Given by AWS publicly)"
"Certificate usally under the termination id-certificate.pem.crt"
"The certificate may take many more code lines than this one"
"-----END CERTIFICATE-----";

const char SECRET_PRIVATE_KEY[] PROGMEM =
"-----BEGIN RSA PRIVATE KEY-----"
"CA certificate here (Given by AWS publicly)"
"Certificate usally under the termination id-private.pem.key"
"The certificate may take many more code lines than this one"
"-----END RSA PRIVATE KEY-----";
