from src.module.defineOs import check_platform
from src.module.linux import screenshoot
from src.gui.drawimage import canvas_gui
from src.module.errorsmsg import *
import src.gui.settings as settings

class shooter:
    this_platform = check_platform().platform

    def start(self):
        if self.this_platform is None:
            dont_define_platform()
            return False
        else:
            self.shoot()

    def shoot(self):
        if self.this_platform == 'linux':
            # use linux module
            try:
                shoot = screenshoot().shoot()
                canvas_gui.show(image=shoot)
            except FileNotFoundError:
                select_folder()
                settings.show(True)

        elif self.this_platform == 'darwin':
            # TODO use macos module
            pass
        else:
            went_wrong()
            pass
