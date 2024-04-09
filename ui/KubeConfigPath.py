import inquirer


def ask_for_kube_config_path() -> str:
    """
    Asks the user for the path of the kube config file.

    """
    questions = [
        inquirer.Text('kube_config_path',
                        message="Enter the path of the kube config file [blank for default config]",
                        default=""),
    ]

    answers = inquirer.prompt(questions)
    return answers['kube_config_path']