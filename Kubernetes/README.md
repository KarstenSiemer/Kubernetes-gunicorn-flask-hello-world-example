# [Kubernetes](https://github.com/kubernetes/kubernetes) [deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) using [Kustomize3](https://github.com/kubernetes-sigs/kustomize)
Here you'll find two folders:
* base
  * this is the skeleton of our deployment.
  * all files from this directory will always end up in our finished manifest
* overlays
  * monitoring-statsd
    * It is directly pulling the manifest declared in the base
    * Our container does not have a possibility of monitoring build into it
    * Here we patch the deployment object to include new args to our gunicorn process and also add a [sidecar](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/) [container](https://en.wikipedia.org/wiki/Docker_(software)), namely [statsd](https://github.com/statsd/statsd)
      also we create a [configmap](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#create-a-configmap) where the configuration of [statsd](https://github.com/statsd/statsd) will be stored. This is done via a [configMapGenerator](https://github.com/kubernetes-sigs/kustomize/blob/master/examples/configGeneration.md) because 
      [kustomize](https://github.com/kubernetes-sigs/kustomize) is nice enough to add a hash at the end of the name of the [configmap](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)
      if this config is changed, the hash changes inside the [deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) template for the pod which in return rolls the pod and reconfigures [statsd](https://github.com/statsd/statsd)
  * prometheus-servicemonitor-crd
    * It is pulling the manifest declared in monitoring-statsd
    * Depending on the setup of your kubernetes cluster, you'll maybe use the [prometheus-operator](https://github.com/coreos/prometheus-operator)
    * The operator installs a [CRD](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) into your cluster which can only be read if the operator is installed
    * Without the operator the manifest including this overlay is invalid
    * A [servicemonitor](https://github.com/coreos/prometheus-operator/blob/master/Documentation/user-guides/getting-started.md) will be used to configure prometheus to scrape our target
  * dev/stage/prod
    * These are the actual overlays from which you'll build the finished manifest
    * They pull the manifest from prometheus-servicemonitor-crd. Reconfigure the resource to monitoring-statsd or create an additional overlay to get the manifest that you need for your environment
    * Here are namePrefixes set, they make it easier to look at all logs from all pods of this deployment using a tool like [stern](https://github.com/wercker/stern)
      Additionally they make the view of `kubectl get pods` more beautiful because it is sorted alphabetically so that prefixed pods are bundled in view. This bundling will happen either way if your are only using one component like here, but imagine having several deployments and statefulsets will completly different names apart from the prefix.
    * I'd suggest that you'll use an ci/cd tool like [argocd](https://github.com/argoproj/argo-cd) to deploy such a manifest
  
