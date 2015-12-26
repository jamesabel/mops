
import platform
import os
import shutil

mops_installers_folder = 'mops_installers'
mops_installer_base = 'mops_installer.exe'

if not os.path.exists(mops_installers_folder):
    os.makedirs(mops_installers_folder)

p = platform.platform()

print('windows platform:%s' % p)

ps = p.lower().split('-')

if ps[0] == 'windows':
    version = ps[1]
    src = os.path.join(mops_installers_folder, mops_installer_base)
    dst = os.path.join(mops_installers_folder, 'mops_installer_win' + str(version) +  '.exe')
    print('moving %s to %s' % (src, dst))
    shutil.move(src, dst)
else:
    print('error:could not determine windows version')

