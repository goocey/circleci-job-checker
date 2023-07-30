## これは

CircleCIの起動中のworkflowでJobが指定時間以上起動していないかをチェックするためのCronJobです

## 起動方法

- kube/secrets/emptyをもとにcircleci_secretを作成
- make build push applyを実行

