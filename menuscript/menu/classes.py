import Foundation
import AppKit
import os

from Foundation import (
    NSDate,
    NSTimer,
    NSRunLoop,
    NSDefaultRunLoopMode,
    NSSearchPathForDirectoriesInDomains,
    NSMakeRect,
    NSLog,
    NSObject,
    NSMutableDictionary,
    NSString,
    NSUserDefaults,
)
from AppKit import (
    NSApplication,
    NSStatusBar,
    NSMenu,
    NSMenuItem,
    NSAlert,
    NSTextField,
    NSSecureTextField,
    NSImage,
    NSSlider,
    NSSize,
    NSWorkspace,
    NSWorkspaceWillSleepNotification,
    NSWorkspaceDidWakeNotification,
)
from PyObjCTools import AppHelper

import weakref

from rumps.compat import text_type, string_types, iteritems, collections_abc
from rumps.text_field import Editing, SecureEditing
from rumps.utils import ListDict

from rumps import _internal
from rumps import events
from rumps import notifications

_TIMERS = weakref.WeakKeyDictionary()
separator = object()


def _nsimage_from_file(filename, dimensions=None, template=None):
    """Take a path to an image file and return an NSImage object."""
    try:
        with open(filename):
            pass
    except (
        IOError
    ):  # literal file path didn't work -- try to locate image based on main script path
        try:
            from __main__ import __file__ as main_script_path

            main_script_path = os.path.dirname(main_script_path)
            filename = os.path.join(main_script_path, filename)
        except ImportError:
            pass
        with open(filename):  # file doesn't exist
            pass  # otherwise silently errors in NSImage which isn't helpful for debugging
    image = NSImage.alloc().initByReferencingFile_(filename)
    image.setScalesWhenResized_(True)
    image.setSize_((20, 20) if dimensions is None else dimensions)
    if template is not None:
        image.setTemplate_(template)
    return image


class Window(object):
    """Generate a window to consume user input in the form of both text and button clicked.

    .. versionchanged:: 0.2.0
        Providing a `cancel` string will set the button text rather than only using text "Cancel". `message` is no
        longer a required parameter.

    .. versionchanged:: 0.3.0
        Add `secure` text input field functionality.

    :param message: the text positioned below the `title` in smaller font. If not a string, will use the string
                    representation of the object.
    :param title: the text positioned at the top of the window in larger font. If not a string, will use the string
                  representation of the object.
    :param default_text: the text within the editable textbox. If not a string, will use the string representation of
                         the object.
    :param ok: the text for the "ok" button. Must be either a string or ``None``. If ``None``, a default
               localized button title will be used.
    :param cancel: the text for the "cancel" button. If a string, the button will have that text. If `cancel`
                   evaluates to ``True``, will create a button with text "Cancel". Otherwise, this button will not be
                   created.
    :param dimensions: the size of the editable textbox. Must be sequence with a length of 2.
    :param secure: should the text field be secured or not. With ``True`` the window can be used for passwords.
    """

    def __init__(
        self,
        message="",
        title="",
        default_text="",
        ok=None,
        cancel=None,
        dimensions=(320, 160),
        secure=False,
    ):
        message = text_type(message)
        message = message.replace("%", "%%")
        title = text_type(title)

        self._cancel = bool(cancel)
        self._icon = None

        _internal.require_string_or_none(ok)
        if not isinstance(cancel, string_types):
            cancel = "Cancel" if cancel else None

        self._alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
            title, ok, cancel, None, message
        )
        self._alert.setAlertStyle_(0)  # informational style

        if secure:
            self._textfield = SecureEditing.alloc().initWithFrame_(
                NSMakeRect(0, 0, *dimensions)
            )
        else:
            self._textfield = Editing.alloc().initWithFrame_(
                NSMakeRect(0, 0, *dimensions)
            )

        self._textfield.setSelectable_(True)
        self._alert.setAccessoryView_(self._textfield)

        self.default_text = default_text

    @property
    def title(self):
        """The text positioned at the top of the window in larger font. If not a string, will use the string
        representation of the object.
        """
        return self._alert.messageText()

    @title.setter
    def title(self, new_title):
        new_title = text_type(new_title)
        self._alert.setMessageText_(new_title)

    @property
    def message(self):
        """The text positioned below the :attr:`title` in smaller font. If not a string, will use the string
        representation of the object.
        """
        return self._alert.informativeText()

    @message.setter
    def message(self, new_message):
        new_message = text_type(new_message)
        self._alert.setInformativeText_(new_message)

    @property
    def default_text(self):
        """The text within the editable textbox. An example would be

            "Type your message here."

        If not a string, will use the string representation of the object.
        """
        return self._default_text

    @default_text.setter
    def default_text(self, new_text):
        new_text = text_type(new_text)
        self._default_text = new_text
        self._textfield.setStringValue_(new_text)

    @property
    def icon(self):
        """The path to an image displayed for this window. If set to ``None``, will default to the icon for the
        application using :attr:`rumps.App.icon`.

        .. versionchanged:: 0.2.0
           If the icon is set to an image then changed to ``None``, it will correctly be changed to the application
           icon.

        """
        return self._icon

    @icon.setter
    def icon(self, icon_path):
        new_icon = _nsimage_from_file(icon_path) if icon_path is not None else None
        self._icon = icon_path
        self._alert.setIcon_(new_icon)

    def add_button(self, name):
        """Create a new button.

        .. versionchanged:: 0.2.0
           The `name` parameter is required to be a string.

        :param name: the text for a new button. Must be a string.
        """
        _internal.require_string(name)
        self._alert.addButtonWithTitle_(name)

    def add_buttons(self, iterable=None, *args):
        """Create multiple new buttons.

        .. versionchanged:: 0.2.0
           Since each element is passed to :meth:`rumps.Window.add_button`, they must be strings.

        """
        if iterable is None:
            return
        if isinstance(iterable, string_types):
            self.add_button(iterable)
        else:
            for ele in iterable:
                self.add_button(ele)
        for arg in args:
            self.add_button(arg)

    def run(self):
        """Launch the window. :class:`rumps.Window` instances can be reused to retrieve user input as many times as
        needed.

        :return: a :class:`rumps.rumps.Response` object that contains the text and the button clicked as an integer.
        """
        if (
            NSUserDefaults.standardUserDefaults().stringForKey_("AppleInterfaceStyle")
            == "Dark"
        ):
            self._alert.window().setAppearance_(
                AppKit.NSAppearance.appearanceNamed_("NSAppearanceNameVibrantDark")
            )  # Adjustment for dark mode

        clicked = self._alert.runModal() % 999
        if clicked > 2 and self._cancel:
            clicked -= 1
        self._textfield.validateEditing()
        text = self._textfield.stringValue()
        self.default_text = self._default_text  # reset default text
        return Response(clicked, text)


class Response(object):
    """Holds information from user interaction with a :class:`rumps.Window` after it has been closed."""

    def __init__(self, clicked, text):
        self._clicked = clicked
        self._text = text

    def __repr__(self):
        shortened_text = self._text if len(self._text) < 21 else self._text[:17] + "..."
        return "<{0}: [clicked: {1}, text: {2}]>".format(
            type(self).__name__, self._clicked, repr(shortened_text)
        )

    @property
    def clicked(self):
        """Return a number representing the button pressed by the user.

        The "ok" button will return ``1`` and the "cancel" button will return ``0``. This makes it convenient to write
        a conditional like,

        .. code-block:: python

            if response.clicked:
                do_thing_for_ok_pressed()
            else:
                do_thing_for_cancel_pressed()

        Where `response` is an instance of :class:`rumps.rumps.Response`.

        Additional buttons added using methods :meth:`rumps.Window.add_button` and :meth:`rumps.Window.add_buttons`
        will return ``2``, ``3``, ... in the order they were added.
        """
        return self._clicked

    @property
    def text(self):
        """Return the text collected from the user."""
        return self._text


class EditName(Window):
    def __init__(self, name: str):
        super().__init__(
            message="",
            title="",
            default_text=name,
            ok="Save Changes",
            cancel="Cancel",
            dimensions=(220, 20),
            secure=False,
        )


class EditSource:
    def __init__(self, name: str):
        super().__init__(
            message="",
            title="",
            default_text=name,
            ok="Rename",
            cancel="Cancel",
            dimensions=(220, 20),
            secure=False,
        )


class EditInterpreter:
    def __init__(self, name: str):
        super().__init__(
            message="",
            title="",
            default_text=name,
            ok="Rename",
            cancel="Cancel",
            dimensions=(220, 20),
            secure=False,
        )
