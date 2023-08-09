# window.py
#
# Copyright 2023 Nokse
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import GObject
from gi.repository import Adw
from gi.repository import Gtk, Gio

class Country(GObject.Object):
    __gtype_name__ = "Country"

    def __init__(self, country_id, country_name, country_capital):
        super().__init__()

        self._country_id = country_id
        self._country_name = country_name
        self._country_capital = country_capital

    @GObject.Property(type=str)
    def country_id(self):
        return self._country_id

    @GObject.Property(type=str)
    def country_name(self):
        return self._country_name

    @GObject.Property(type=str)
    def country_capital(self):
        return self._country_capital

    def __repr__(self):
        return f"Country(country_id={self.country_id}, country_name={self.country_name})"

class GtkcolumnviewExampleWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'GtkcolumnviewExampleWindow'

    label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        nodes = {
            "nl": ("Netherlands", "Amsterdam"),
            "br": ("Brazil", "Brasília"),
            "fi": ("Finland", "Helsinki"),
            "mx": ("Mexico", "Mexico City"),
            "hu": ("Hungary", "Budapest"),
            "in": ("India", "New Delhi"),
            "au": ("Austria", "Vienna"),
            "om": ("Oman", "Muscat"),
            "eg": ("Egypt", "Cairo"),
            "de": ("Germany", "Berlin"),
            "pt": ("Portugal", "Lisbon"),
            "ca": ("Canada", "Ottawa"),
            "jp": ("Japan", "Tokyo"),
            "kr": ("Korea", "Seoul"),
            "ls": ("Lesotho", "Maseru"),
            "dk": ("Denmark", "Copenhagen"),
        }

        self.model = Gio.ListStore()

        self.cv = Gtk.ColumnView()

        self.row_filter = Gtk.CustomFilter()
        self.row_filter.set_filter_func(self.filter)
        tree_model_filter = Gtk.FilterListModel(model=self.model)
        tree_model_filter.set_filter(self.row_filter)

        tree_model = Gtk.TreeListModel.new(tree_model_filter, False, True, self.model_func)
        tree_sorter = Gtk.TreeListRowSorter.new(self.cv.get_sorter())

        self.entry = Gtk.Entry(margin_start=6, margin_end=6, margin_top=6, margin_bottom=6)
        self.entry.connect("activate", self.filter_rows)

        sorter_model = Gtk.SortListModel(model=tree_model, sorter=tree_sorter)
        selection = Gtk.SingleSelection.new(model=sorter_model)
        self.cv.set_model(selection)

        # list store -> filter -> tree list model -> sorter_model -> single selection -> column view
        for n in nodes.keys():
            self.model.append(Country(country_id=n, country_name=nodes[n][0], country_capital=nodes[n][1]))

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_factory_setup)
        factory.connect("bind", self._on_factory_bind, "country_name")

        factory2 = Gtk.SignalListItemFactory()
        factory2.connect("setup", self._on_factory_setup)
        factory2.connect("bind", self._on_factory_bind, "country_capital")

        col1 = Gtk.ColumnViewColumn(title="Country", factory=factory)
        col1.props.expand = True
        self.cv.append_column(col1)

        col2 = Gtk.ColumnViewColumn(title="Head of State", factory=factory2)
        col2.props.expand = True
        self.cv.append_column(col2)

        sorter = Gtk.CustomSorter.new(self.sort_func, user_data="country_name")
        col1.set_sorter(sorter)

        self.cv.props.hexpand = True
        self.cv.props.vexpand = True

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, valign=Gtk.Align.FILL)
        box.append(Adw.HeaderBar(css_classes=["flat"]))

        box.append(self.entry)
        scroll = Gtk.ScrolledWindow(vexpand=True)
        scroll.set_child(self.cv)
        box.append(scroll)

        self.set_default_size(1000, 700)
        self.set_content(box)

    def filter_rows(self, entry):
        self.row_filter.changed(Gtk.FilterChange.DIFFERENT)

    def filter(self, data):
        text = self.entry.get_text()
        if text == "":
            return 1
        if text.lower() in data.country_name.lower():
            return 1
        return 0

    def model_func(self, arg):
        pass

    def sort_func(self, obj_1, obj_2, data):
        if data == "country_name":
            if obj_1.country_name.lower() < obj_2.country_name.lower():
                return -1
            elif obj_1.country_name.lower() == obj_2.country_name.lower():
                return 0
            return 1
        return 0

    def _on_factory_setup(self, factory, list_item):
        cell = Gtk.Inscription()
        cell._binding = None
        list_item.set_child(cell)

    def _on_factory_bind(self, factory, list_item, what):
        cell = list_item.get_child()
        country = list_item.get_item().get_item()
        cell._binding = country.bind_property(what, cell, "text", GObject.BindingFlags.SYNC_CREATE)

    def _on_factory_unbind(self, factory, list_item, what):
        cell = list_item.get_child()
        if cell._binding:
            cell._binding.unbind()
            cell._binding = None

    def _on_selected_item_notify(self, dropdown, _):
        country = dropdown.get_selected_item()
        print(f"Selected item: {country}")

    def _on_factory_setup(self, factory, list_item):
        cell = Gtk.Inscription()
        cell._binding = None
        list_item.set_child(cell)

    def _on_factory_bind(self, factory, list_item, what):
        cell = list_item.get_child()
        country = list_item.get_item().get_item()
        cell._binding = country.bind_property(what, cell, "text", GObject.BindingFlags.SYNC_CREATE)

    def _on_selected_item_notify(self, dropdown, _):
        country = dropdown.get_selected_item()
        print(f"Selected item: {country}")
