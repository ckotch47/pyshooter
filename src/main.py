from src.module.defineOs import check_platform
from src.gui.drawimage import canvas_gui
from src.module.errorsmsg import *
import src.gui.settings as settings

var = check_platform().platform
if var == 'linux':
    from src.module.shot.linux import screenshoot
elif var == 'darwin':
    from src.module.shot.darwin import screenshoot


class shooter:
    this_platform = var

    def start(self):
        if self.this_platform is None:
            dont_define_platform()
            return False
        else:
            self.shoot()

    @staticmethod
    def shoot():
        try:
            shoot = screenshoot().shoot()
            canvas_gui.show(image=shoot)
        except FileNotFoundError:
            select_folder()
            settings.show(True)
