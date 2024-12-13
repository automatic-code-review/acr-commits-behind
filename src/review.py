import automatic_code_review_commons as commons


def review(config):
    commits_behind = config['merge']['commits_behind']

    comments = []
    commits_behind_current = len(commits_behind)
    commits_behind_limit = config["commitsBehindLimit"]

    if commits_behind_current > commits_behind_limit:
        descr_message = config['message']
        descr_message = descr_message.replace("${COMMITS_BEHIND}", str(commits_behind_current))
        descr_message = descr_message.replace("${COMMITS_BEHIND_LIMIT}", str(commits_behind_limit))

        comment = commons.comment_create(
            comment_id=commons.comment_generate_id(descr_message),
            comment_description=descr_message,
            comment_path=None,
            comment_snipset=False,
        )

        if 'processorArgs' in config:
            comment['processorArgs'] = config['processorArgs']

        comments.append(comment)

    return comments
