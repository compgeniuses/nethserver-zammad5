==================
nethserver-zammad5
==================

Zammad is a web-based, open source user support/ticketing solution.
Zammad 5 is provided as docker installation.

Custom URLs
===========

Just create a file like `/etc/httpd/conf.d/zammadcustom.conf` with following content. Replace example.org with the custom URL.::

   <VirtualHost *:80>
       IncludeOptional conf.d/default-virtualhost.inc
   </VirtualHost>

   <VirtualHost *:80>
       ServerName example.org
       RedirectMatch 301 ^(?!/.well-known/acme-challenge/).* https://example.org
   </VirtualHost>

   <VirtualHost *:443>
       SSLEngine on
       SSLProtocol all -SSLv2 -SSLv3
       SSLCipherSuite EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH

       RewriteEngine On
       RewriteCond %{HTTP_HOST} example.org
       RewriteRule (assets|api)/(.*) /$1/$2 [PT]
       RewriteCond %{HTTP_HOST} example.org
       RewriteRule (.*) /help$1 [PT]

       # CSRF token fix - thanks to CptCharlesG
       RequestHeader set X_FORWARDED_PROTO 'https'
       RequestHeader set X-Forwarded-Ssl on

       SetEnvIf Request_URI "(.*)" ORIGINAL_URL=$1
       RequestHeader add X-ORIGINAL-URL %{ORIGINAL_URL}e

       # replace 'localhost' with your fqdn if you want to use zammad from remote
       ServerName example.org

       ## don't loose time with IP address lookups
       HostnameLookups Off

       ## needed for named virtual hosts
       UseCanonicalName Off

       ## configures the footer on server-generated documents
       ServerSignature Off
       ProxyRequests Off
       ProxyPreserveHost On

       ProxyPass / http://localhost:8080/
       ProxyPassReverse / http://localhost:8080/
   </VirtualHost>

You may use multiple files.
