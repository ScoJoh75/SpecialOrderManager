from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, sudo
import random

REPO_URL = 'https://ScoJoh75@bitbucket.org/ScoJoh75/special-order-manager.git'
COLORS = {'PURPLE': '\033[95m', 'CYAN': '\033[96m', 'DARKCYAN': '\033[36m',
          'BLUE': '\033[94m', 'GREEN': '\033[92m', 'YELLOW': '\033[93m',
          'RED': '\033[91m', 'BOLD': '\033[1m', 'UNDERLINE': '\033[4m',
          'END': '\033[0m', }

# Set the color for printed messages
MSG_COLOR = COLORS['BOLD']


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    _install_java()
    _install_nginx()
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _apply_patch_to_jaydebeapi(source_folder)
    _update_static_files(source_folder)
    _update_database(site_folder, source_folder)
    _install_nginx_config(source_folder, env.host, env.user)
    _install_systemd_service(source_folder, env.host, env.user, env.wsgi_app)
    _restart_web_services(env.host)
    _finish_up(env.host)


def print_msg(msg_text):
    print(MSG_COLOR + '*' * 79 + '\n' + msg_text + '\n' + '*' * 79 + COLORS['END'])


def _install_java():
    if not exists('/usr/lib/jvm'):
        print_msg('Java is not on this system.  Installing now.')
        sudo('apt-get install openjdk-8-jre-headless -y')
    else:
        print_msg('Java already installed.  Skipping...')


def _install_nginx():
    if not exists('/usr/sbin/nginx'):
        print_msg('Nginx is not on this system.  Installing now.')
        sudo('apt-get install nginx -y')
    else:
        print_msg('Nginx already installed.  Skipping...')


def _create_directory_structure_if_necessary(site_folder):
    print_msg('Creating/checking site directory structure...')
    for subfolder in ('database', 'static', 'media', 'logs', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')
    # Create media subfolders if they do not exist.
    for subfolder in ('machines', 'parts', 'manuals', 'logs', 'pm_documents'):
        run(f'mkdir -p {site_folder}/media/{subfolder}')
    # Create the transaction log file if one does not already exist
    if not exists(site_folder + '/logs/transaction.log'):
        print_msg('Transaction log file not present.  Initializing now...')
        run(f'touch {site_folder}/logs/transaction.log')
    else:
        print_msg('Transaction log already exists.  Skipping...')


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        print_msg('Source folder already exists.  Performing git fetch...')
        run(f'cd {source_folder} && git fetch')
    else:
        print_msg('Source folder is not present.  Cloning from git...')
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_settings(source_folder, site_name):
    print_msg('Updating settings.py for production environment...')
    settings_path = source_folder + '/specialorders/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
        )
    secret_key_file = source_folder + '/specialorders/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    print_msg('Installing/updating virtualenv...')
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        print('Virtualenv does not exist.  Creating now...')
        run(f'python3.6 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')


def _apply_patch_to_jaydebeapi(source_folder):
    # This patch allows proper thread reattachment with JVM for JPype
    print_msg('Patching Jaydebeapi...')
    virtualenv_folder = source_folder + '/../virtualenv'
    run(f'cd {source_folder} && cp deploy_tools/jaydebeapi__init__modified.py '
        f'{virtualenv_folder}/lib/python3.6/site-packages/jaydebeapi/__init__.py')


def _update_static_files(source_folder):
    print_msg('Copying static files into production locations...')
    run(
        f'cd {source_folder}'
        '&& ../virtualenv/bin/python manage.py collectstatic --noinput'
    )


def _update_database(site_folder, source_folder):
    if not exists(site_folder + '/database/db.sqlite3'):
        print_msg('Database file does not exist.  Copying one into place.')
        run(f'cd {source_folder} && cp deploy_tools/db.sqlite3 ../database/')
    else:
        print_msg('Existing database is present, performing migrations...')

    run(
        f'cd {source_folder}'
        '&& ../virtualenv/bin/python manage.py migrate --noinput'
    )


def _install_nginx_config(source_folder, site_name, user_name):
    site_config_file = f'/etc/nginx/sites-available/nginx-{site_name}.conf'
    if not exists(site_config_file):
        print_msg('No site configuration exists for Nginx.  Creating ...')
        sudo(f'cd {source_folder} && cp deploy_tools/nginx.template.conf {site_config_file}')
        sed(site_config_file, 'SITENAME', site_name, use_sudo=True)
        sed(site_config_file, 'USERNAME', user_name, use_sudo=True)
        sudo(f'ln -s {site_config_file} /etc/nginx/sites-enabled/{site_name}')
    if exists('/etc/nginx/sites-enabled/default'):
        print_msg('Removing default Nginx configuration...')
        sudo('rm /etc/nginx/sites-enabled/default')


def _install_systemd_service(source_folder, sitename, username, wsgi_app):
    service_file = f'gunicorn-{sitename}.service'
    if not exists(f'/etc/systemd/system/{service_file}'):
        print_msg('No gunicorn service exists.  Creating systemd service now...')
        sudo(f'cd {source_folder}' 
             f'&& cp deploy_tools/gunicorn-systemd.template.service /etc/systemd/system/{service_file}')
        sed(f'/etc/systemd/system/{service_file}', 'SITENAME', sitename, use_sudo=True)
        sed(f'/etc/systemd/system/{service_file}', 'USERNAME', username, use_sudo=True)
        sed(f'/etc/systemd/system/{service_file}', 'SITEAPP', wsgi_app, use_sudo=True)
        sudo('systemctl daemon-reload')


def _restart_web_services(site_name):
    print_msg('Restarting gunicorn and Nginx...')
    sudo(f'systemctl restart gunicorn-{site_name}')
    sudo('systemctl restart nginx')


def _finish_up(site_name):
    print_msg('Site installation and configuration is complete.\n\nYou can view it at http://' + site_name)
