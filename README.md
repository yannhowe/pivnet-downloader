# pivnet-downloader

A python thing to get all your [Pivotal Network](https://network.pivotal.io/) stuff so you don't have to.

# Quickstart
Clone this repository
```
git clone https://github.com/yannhowe/pivnet-downloader
```
1) Make sure you have the amazing [Pipenv](https://docs.pipenv.org/en/latest/). If not, `brew install pipenv` or `pip install --user pipenv`.
2) Log in to your [pivotal profile](https://network.pivotal.io/users/dashboard/edit-profile) and generate your UAA API KEY if you don't already have one and add the UAA API KEY to the .env file
```
cd pivnet-downloader
pipenv run python pivnet-downloader.py
```
You will see a product list similar to the following
```
['p-fim-addon', 'crunchy-postgresql', 'buildpack_suite', 'hazelcast-pcf', 'p-ipsec-addon', 'p-clamav-addon', 'tc-server-3x-core', 'wso2-api-manager', 'vmware-nsx-t', 'service-backups-sdk', 'java-buildpack', 'nginx-buildpack', 'bitdefender-endpoint', 'zettaset-xcrypt', 'pcf-services-sdk', 'p-dataflow', 'big-data', 'pivotal-openjdk', 'gemfirexd', 'p-gateway-dashboard', 'p-spring-cloud-services', 'pivotal-rabbitmq', 'dynatrace-fullstack-addon', 'blue-medora-nozzle', 'pcf-services', 'apm', 'credhub-service-broker', 'p-riak-cs', 'buildpacks', 'service-metrics-sdk', 'altoros-aws-s3', 'redis-enterprise-pack-service-broker', 'nr-firehose-nozzle', 'gcp-stackdriver-nozzle', 'redis-enterprise-pack', 'hazelcast-jet', 'tc-server-buildpack', 'wavefront-nozzle', 'p-cloudcache', 'a9s-logme', 'snyk-service-broker', 'p-spring-flo', 'forgerock', 'snyk', 'pivotal-spring-runtime', 'essential_pks', 'buildpack-extensions', 'p-gemfire', 'p-data-sync', 'minio-internal-blobstore', 'instana-microservices-application-monitoring', 'tc-server-3x-runtimes', 'stemcells', 'evolven-change-analytics', 'pivotal-cf', 'datastax-enterprise-service-broker', 'tc-server-4x-core', 're-tile-manager', 'p-new-relic', 'p-logsearch', 'p-tracker', 'p-ssc-gemfire', 'pivotal-telemetry-collector', 'contrast-security-service-broker', 'pivotal-app-suite', 'pivotal-hd', 'splunk-nozzle', 'tibco-businessworks', 'aquasec', 'pivotal-hdb', 'pivotal-web-server', 'a9s-redis', 'ibm-websphere-liberty', 'p-metrics-forwarder', 'a9s-mysql', 'microsoft-azure-log-analytics-nozzle', 'altoros-elasticsearch', 'p-mysql', 'a9s-mongodb', 'gcp-service-broker', 'snappydata-service', 'p-event-alerts', 'datadog-application-monitoring', 'stemcells-windows-server', 'new-relic-dotnet-buildpack', 'altoros-jenkins', 'pivotal-postgres', 'cyberark-conjur', 'pivotal-gpdb-backup-restore', 'control-tower', 'hwc-buildpack', 'pivotal-hdp', 'signal-sciences-service-broker', 'ecs-service-broker', 'aerospike-ee-on-demand', 'ibm-mq-advanced', 'pivotal-tcserver', 'push-notification-service', 'nodejs-buildpack', 'reliability_view_pcf', 'p-scheduler', 'yugabyte-db', 'pega', 'tc-server-3x-templates', 'tc-server-4x-runtimes', 'riverbed-appinternals', 'p-apache-http-server', 'altoros-log-search', 'harbor-container-registry', 'a9s-rabbitmq', 'ruby-buildpack', 'black-duck-service-broker', 'staticfile-buildpack', 'dotnet-core-buildpack', 'php-buildpack', 'python-buildpack', 'binary-buildpack', 'go-buildpack', 'r-buildpack', 'tc-server-4x-templates', 'pas-for-kubernetes', 'on-demand-services-sdk', 'neo4j-enterprise', 'apigee-edge-for-pcf-service-broker', 'dynatrace', 'vormetric-transparent-encryption', 'platform-automation', 'pcfdev', 'heimdall-database-proxy', 'xcrypt-archive', 'a9s-elasticsearch', 'apigee-edge-installer', 'azure-service-broker', 'altoros-cassandra', 'pivotal_single_sign-on_service', 'minio', 'smb-volume-service', 'altoros-heartbeat', 'mongodb-enterprise-service', 'appdynamics-analytics', 'pagerduty-service-broker', 'p-redis', 'p-compliance-scanner', 'pivotal-gemfire', 'sumologic-nozzle', 'p-concourse', 'cloudbees-core', 'a9s-postgresql', 'synopsys-seeker', 'pcf-automation', 'p-metrics', 'minio-greenplum', 'datadog', 'boomi-data-services', 'solace-pubsub', 'p-rabbitmq', 'twistlock', 'ops-manager', 'elastic-runtime', 'boomi-data-services-pks', 'p-appdynamics', 'pivotal-mysql', 'greenplum-for-kubernetes', 'p-healthwatch', 'aws-services', 'pivotal-container-service', 'pas-windows', 'p-bosh-backup-and-restore', 'p-isolation-segment', 'stemcells-ubuntu-xenial', 'pivotal-function-service', 'pivotal-gpdb', 'pcf-app-autoscaler', 'appdynamics-platform', 'p-windows-runtime']
```
Add the products required to pivnet-downloader.py
For example:
```
products=[
    'p-bosh-backup-and-restore',
    'pivotal-container-service',
    ]
```
> Remember you need to accept the EULA on the website before you are allowed to download using the API!

Run again to download files into `./product-files/`
```
pipenv run python pivnet-downloader.py
```
