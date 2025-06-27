from kubernetes import client, config
import random
import string

class K8s():
    def __init__(self):
        config.load_kube_config()
        self.corev1 = client.CoreV1Api()
        self.batchv1 = client.BatchV1Api()

    def getNamespaces(self) -> list:
        listNamespaces = self.corev1.list_namespace()
        namespaces = []
        for i in listNamespaces.items:
            if not i.metadata.name in namespaces:
                namespaces.append(i.metadata.name)
        namespaces.sort()
        return namespaces

    def getCronJobs(self, namespace: str) -> list:
        listNamespacedCronJob = self.batchv1.list_namespaced_cron_job(namespace=namespace)
        cronJobs = []
        for i in listNamespacedCronJob.items:
            if not i.metadata.name in cronJobs:
                cronJobs.append(i.metadata.name)
        cronJobs.sort()
        return cronJobs
    
    def createJobFromCronJob(self, namespace: str, cronjob: str) -> str:
        readNamespacedCronJob = self.batchv1.read_namespaced_cron_job(name=cronjob, namespace=namespace)
        randomString = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        jobName = "{0}-{1}".format(readNamespacedCronJob.metadata.name, randomString)
        jobSpec = readNamespacedCronJob.spec.job_template.spec
        jobSpec.ttl_seconds_after_finished = 120
        metadata = client.V1ObjectMeta(name=jobName)
        body = client.V1Job(api_version="batch/v1", kind="Job", metadata=metadata, spec=jobSpec)
        self.batchv1.create_namespaced_job(namespace=namespace, body=body)
        return jobName
    
    def currentStatusJob(self, namespace: str, jobName: str) -> str:
        statusText = "-"
        try:
            job = self.batchv1.read_namespaced_job(name=jobName, namespace=namespace)
            if hasattr(job.status, 'active') and job.status.active and job.status.active > 0:
                a = "Active" # Running
            if job.status.conditions:
                for condition in job.status.conditions:
                    if condition.status:
                        if condition.type and job.status.succeeded > 0:
                            statusText = condition.type # Complete
                        else:
                            statusText = "{0} - {1}".format(condition.type, condition.message) # Failed
        except client.exceptions.ApiException as e:
            if e.reason == "Not Found":
                statusText = "Not Found"
        except:
            statusText = "Error getting Status!"
        return statusText
