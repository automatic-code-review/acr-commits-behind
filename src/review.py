from http import HTTPStatus

import automatic_code_review_commons as commons
import requests


def review(config):
    git_url = config['git_url']
    git_token = config['git_token']

    merge = config['merge']
    project_id = merge['project_id']
    from_project_id = merge['from_project_id']
    branch_target = merge['branch']['target']
    branch_source = merge['branch']['source']

    url = (f"{git_url}/api/v4/projects/{project_id}/repository/compare?"
           f"from={branch_source}&to={branch_target}&from_project_id={from_project_id}")

    response = requests.get(url, headers={
        'Private-Token': git_token
    })

    comments = []
    status_code = {response.status_code}

    if status_code == HTTPStatus.OK:
        data = response.json()
        commits_behind = len(data["commits"])
        commits_behind_limit = config["commitsBehindLimit"]

        if commits_behind > commits_behind_limit:
            descr_message = config['message']
            descr_message = descr_message.replace("${COMMITS_BEHIND}", str(commits_behind))
            descr_message = descr_message.replace("${COMMITS_BEHIND_LIMIT}", str(commits_behind_limit))

            comments.append(commons.comment_create(
                comment_id=commons.comment_generate_id(descr_message),
                comment_description=descr_message,
                comment_path=None
            ))
    else:
        raise OSError(f"Não foi possivel buscar os commits behind. Status code {status_code}")

    return comments
