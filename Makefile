kubeconfig = $(shell kubectl config current-context)
kubeenv = $(shell echo ${kubeconfig} | sed -e's/k3d-//g')

build:
	docker build -t docker-registry.dev.g00cey/circleci-job-checker:latest . -f kube/Dockerfile
push: build
	docker push docker-registry.dev.g00cey/circleci-job-checker:latest

apply:
	-@kubectl create namespace circleci-job-checker
	-@kubectl -n circleci-job-checker delete secret circleci
	-@kubectl -n circleci-job-checker create secret generic circleci --from-env-file ./kube/secrets/circleci_secret
	helmfile -f ./kube/helmfiles.yml -e $(kubeenv) apply

delete:
	helmfile -f ./kube/helmfiles.yml -e $(kubeenv) delete

exec: apply
	-@kubectl -n circleci-job-checker delete job.batch job1
	kubectl -n circleci-job-checker create job job1 --from=cronjob/check-circleci
