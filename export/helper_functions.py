import os
import shutil
import tempfile
from subprocess import Popen, PIPE

from django.template.loader import get_template


class LaTeX:
    """
    https://github.com/d120/pyophase/blob/master/ophasebase/helper.py
    Retrieved 10.08.2020
    """
    @staticmethod
    def render(context, template_name, assets, app='export', external_assets=None):
        template = get_template(template_name)
        rendered_tpl = template.render(context).encode('utf-8')
        with tempfile.TemporaryDirectory() as tempdir:
            # for asset in assets:
            #     shutil.copy(os.path.dirname(os.path.realpath(__file__)) + '/../' + app + '/assets/' + asset, tempdir)
            # if external_assets is not None:
            #     for asset in external_assets:
            #         shutil.copy(asset, tempdir)
            process = Popen(['pdflatex'], stdin=PIPE, stdout=PIPE, cwd=tempdir, )
            pdflatex_output = process.communicate(rendered_tpl)
            try:
                with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as f:
                    pdf = f.read()
            except FileNotFoundError:
                pdf = None
        return pdf, pdflatex_output
