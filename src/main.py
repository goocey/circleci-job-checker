from pycircleci.api import Api, CIRCLE_TOKEN, CIRCLE_API_URL
from os import environ
import slackweb
import textwrap


org = environ.get("ORG")
project = environ.get("PROJECT")
limit_exec_job_second = environ.get("LIMIT_EXEC_JOB_SECOND")
slack_webhook = environ.get("SLACK_WEBHOOK")

circle_client = Api(token=CIRCLE_TOKEN, url=CIRCLE_API_URL)
# get current user info
circle_client.get_user_info()
# get list of projects
results = circle_client.get_project_build_summary(org, project, status_filter="running")
# pretty print results as json
# circle_client.ppj(results)
for result in results:
    if (int(result["build_time_millis"]) > int(limit_exec_job_second) * 1000):
        # print(result["workflows"]["workflow_name"])
        # print(result["start_time"])
        # print(result["build_num"])
        # print(result["build_time_millis"])
        # print(result["build_url"])
        total_sec = int(result["build_time_millis"]) / 1000
        min = int(total_sec // 60)
        sec = int(total_sec % 60)
        string = """
        {workflow_name} が {start} 開始で {build_time} 実行されています。
        {build_url}
        """
        slack = slackweb.Slack(url=slack_webhook)
        text = textwrap.dedent(string).format(
            workflow_name=result["workflows"]["workflow_name"],
            start=result["start_time"],
            build_num=result["build_num"],
            build_time="{min}分 {sec}秒".format(min=min,sec=sec),
            build_url=result["build_url"]
        ).strip()
        slack.notify(text=text)
    else:
        pass

# pretty print the details of the last request/response
# circle_client.ppr()