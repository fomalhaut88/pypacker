import os
import platform
import shutil


py_version = platform.python_version()
if py_version[0] != '3':
    print("Unsupported python version:", py_version)
    exit()


TEMPLATES_DIR = os.path.normpath(os.path.join(
    os.path.dirname(__file__),
    '..',
    'templates'
))


def input_not_empty(prompt):
    value = ''
    while not value:
        value = input(prompt).strip()
    return value


def input_file(prompt):
    path = ''
    while not (os.path.exists(path) and os.path.isfile(path)):
        path = input_not_empty(prompt)
    return path


def get_template(name):
    path = os.path.join(TEMPLATES_DIR, name)
    with open(path) as f:
        return f.read()


def create_by_template(tpl_name, params, file_path):
    tpl = get_template(tpl_name)
    content = tpl % params
    with open(file_path, 'w') as f:
        f.write(content)


def enter_params():
    params = {}
    params['name'] = input_not_empty("Enter the name of program: ")
    params['author'] = input_not_empty("Enter author or publicher: ")
    params['url'] = input_not_empty("Enter URL: ")
    params['email'] = input_not_empty("Enter Email: ")
    params['description'] = input_not_empty("Enter short description: ")
    params['version'] = input_not_empty("Enter version: ")
    return params


def add_icon(params):
    icon_path = input_file("Specify path to icon: ")
    icon_name = params['name'] + '.ico'
    print("Copying {} -> {} ...".format(icon_path, icon_name))
    shutil.copyfile(icon_path, icon_name)


def choose_main(params):
    params['main'] = input_file("Specify path to main: ")


def add_version(params):
    print("Adding version file ...")
    with open('version', 'w') as f:
        f.write(params['version'])


def list_platforms(params):
    platforms_str = input_not_empty("List platforms separated by comma (example: windows64,ubuntu64): ")
    params['platforms'] = [
        item.strip().lower()
        for item in platforms_str.split(',')
    ]


def create_spec(params):
    create_by_template(
        'spec.tpl',
        {
            'name': params['name'],
            'icon': params['name'] + '.ico',
            'main': params['main'],
        },
        params['name'] + '.spec'
    )


def create_iss(params):
    create_by_template(
        'windows-iss.tpl',
        {
            'name': params['name'],
            'Name': params['name'].title(),
            'icon': params['name'] + '.ico',
            'version': params['version'],
            'url': params['url'],
            'author': params['author'],
        },
        'windows/{}-setup.iss'.format(params['name'])
    )


def create_windows64_build(params):
    create_by_template(
        'windows-build-cmd.tpl',
        {
            'name': params['name'],
        },
        'build-windows64.cmd'
    )


def create_control(params):
    create_by_template(
        'ubuntu-control.tpl',
        {
            'name': params['name'],
            'Name': params['name'].title(),
            'version': params['version'],
            'email': params['email'],
            'author': params['author'],
            'description': params['description'],
        },
        'linux/control'
    )


def create_desktop(params):
    create_by_template(
        'ubuntu-desktop.tpl',
        {
            'name': params['name'],
            'Name': params['name'].title(),
            'icon': params['name'] + '.ico',
            'description': params['description'],
        },
        'linux/{}.desktop'.format(params['name'])
    )


def create_ubuntu64_build(params):
    create_by_template(
        'ubuntu-build-sh.tpl',
        {
            'name': params['name'],
            'icon': params['name'] + '.ico',
        },
        'build-ubuntu64.sh'
    )


def main():
    print("Welcome to pypacker.")
    print("Below it will help you to prepare your project for building for different platforms.")

    params = enter_params()

    add_icon(params)
    choose_main(params)
    add_version(params)
    list_platforms(params)
    create_spec(params)

    if 'windows64' in params['platforms']:
        os.makedirs('windows', exist_ok=True)
        create_iss(params)
        create_windows64_build(params)

    if 'ubuntu64' in params['platforms']:
        os.makedirs('linux', exist_ok=True)
        create_control(params)
        create_desktop(params)
        create_ubuntu64_build(params)

    print("Completed")
