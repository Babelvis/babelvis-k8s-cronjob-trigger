from kubernetes import client, config
import random
import string

class K8s():
    def __init__(self):
        config.load_kube_config()
        self.corev1 = client.CoreV1Api()
        self.batchv1 = client.BatchV1Api()

    def getNamespaces(self):
        listNamespaces = self.corev1.list_namespace()
        namespaces = []
        for i in listNamespaces.items:
            if not i.metadata.name in namespaces:
                namespaces.append(i.metadata.name)
        namespaces.sort()
        return namespaces

    def getCronJobs(self, namespace: str):
        listNamespacedCronJob = self.batchv1.list_namespaced_cron_job(namespace=namespace)
        cronJobs = []
        for i in listNamespacedCronJob.items:
            if not i.metadata.name in cronJobs:
                cronJobs.append(i.metadata.name)
        cronJobs.sort()
        return cronJobs
    
    def createJobFromCronJob(self, namespace: str, cronjob: str):
        readNamespacedCronJob = self.batchv1.read_namespaced_cron_job(name=cronjob, namespace=namespace)
        randomString = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        metadata = client.V1ObjectMeta(name="{0}-{1}".format(readNamespacedCronJob.metadata.name, randomString) )
        body = client.V1Job(api_version="batch/v1", kind="Job", metadata=metadata, spec=readNamespacedCronJob.spec.job_template.spec)
        return self.batchv1.create_namespaced_job(namespace=namespace, body=body)
