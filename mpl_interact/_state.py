# -*- coding: utf-8 -*-

from mpl_events import mpl
from ._base import InteractorBase, KeyModifier


class AxesLimitsResetInteractor(InteractorBase):

    keys = ['h', 'home']

    def reset_axes_limits(self, axes: mpl.Axes):
        """Resets limits for given axes
        """
        if not axes:
            return

        axes.relim()
        axes.set_xlim(auto=True)
        axes.set_ylim(auto=True)
        axes.autoscale_view(scalex=True, scaley=True)

        self.update()

    def on_mouse_button_press(self, event: mpl.MouseEvent):
        if event.dblclick:
            self.reset_axes_limits(event.inaxes)

    def on_key_release(self, event: mpl.KeyEvent):
        key = self.parse_key(event.key)

        if self.check_key(key, self.keys, KeyModifier.NO):
            self.reset_axes_limits(event.inaxes)
