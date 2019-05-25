# -*- coding: utf-8 -*-

from mpl_events import mpl
from ._base import InteractorBase


class AxesLimitsResetInteractor(InteractorBase):

    key = 'h'

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
        if event.key == self.key:
            self.reset_axes_limits(event.inaxes)
